import logging
import os
import traceback
import jmespath
from time import time
from bson.json_util import dumps, loads
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, UNAUTHORIZED, OK

from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import json as json_response
from sanic_jwt_extended import jwt_optional
from sanic_jwt_extended.tokens import Token
from xpms_common.errors import XpmsError
from xpms_common.xpms_logger import XPMSContext, XPMSLogger

from core.config.constants import SERVICE_NAME, TMBR_CSBD_DETAILS, TMBR_GBD_DETAILS, REF_MASTER_MAP
from apps.rules.advance_search import advnce_rulesets_search
from apps.rules.get_prod_claim import FetchClaim
from apps.rules.get_prod_claim_postgres import FetchClaimPg
from apps.rules.trigger_rules import TriggerRules
from apps.rules.support_line_save import update_refdb_mapping
from xpms_storage.db_handler import DBProvider

logger = XPMSLogger.get_instance()
tmbrui_apis_bp = Blueprint("tmbrui_apis_bp")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def set_formatter():
    format_string = (
        '{"log_level": "%(levelname)s", '
        '"filename": "%(filename)s", '
        '"function": "%(funcName)s", '
        '"timestamp": "%(asctime)s", '
        '"line_no": "%(lineno)d", '
        '"message": "%(message)s"}'
    )
    formatter = logging.Formatter(format_string)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

if not log.handlers:
    set_formatter()

context = XPMSContext(
    solution_id="",
    service_name=SERVICE_NAME,
    method_name="console.endpoint.entity_config",
)

@tmbrui_apis_bp.route("/ref_data_diff", methods=["GET", "OPTIONS"])
async def ref_data_diff(request):
    ref_details = REF_MASTER_MAP.get(request.args.get("source", "").lower())
    if not ref_details:
        return json_response(
            {
                "error_message": "Unknown Table Name",
                "status_code": BAD_REQUEST,
            },
            status=BAD_REQUEST,
        )

    db_name, col_name = ref_details.get("name", "").split("/")
    db_handler = DBProvider.get_instance(db_name=db_name)
    tmp_data = db_handler.find(table="reft_" + col_name.strip(), filter_obj={"is_deleted": False})
    tmp_data = list(tmp_data) if tmp_data else []
    unique_ids = jmespath.search(f"[].{ref_details['unique_key']}", tmp_data)
    master_data = db_handler.find(table="refm_" + col_name, filter_obj={ref_details["unique_key"]: {"$in": unique_ids}})
    master_data = list(master_data) if master_data else []
    diff_resp = []

    for id in set(unique_ids):
        m_record = jmespath.search(f"[?{ref_details['unique_key']} == `{id}`] | [0]", master_data)
        t_record = jmespath.search(f"[?{ref_details['unique_key']} == `{id}`] | [0]", tmp_data)
        diff = {}
        if not m_record:
            diff["new_record_added"] = {
                ref_details["unique_key"]: id,
                "new_value": t_record,
                "old_value": None,
            }
        diff_resp.append(diff)

    return json_response(diff_resp, dumps=dumps)

@tmbrui_apis_bp.route("/edit_trigger", methods=["POST", "OPTIONS"], name="editTrigger")
async def edit_trigger(request):
    try:
        payload = request.json
        if not payload:
            return json_response(
                {
                    "error_message": "Missing Payload Information",
                    "status_code": BAD_REQUEST,
                },
                status=BAD_REQUEST,
            )

        auth_info = request.json.pop("auth", {})
        if auth_info.get("user_roles", {}).get("re_role") != "super":
            return json_response(
                {
                    "error_message": "Invalid auth information. Access denied.",
                    "status_code": UNAUTHORIZED,
                },
                status=UNAUTHORIZED,
            )

        ruleset_id = payload["data"].get("ruleset_id", "")
        ruleset_metadata = payload["data"].get("ruleset_metadata", {})
        if ruleset_metadata.get("support_line"):
            # Save RefDB Hist Look UP criteria
            update_refdb_mapping(inp_data=payload["data"])

        if ruleset_id.upper().startswith("PSME"):
            response_data = {
                "headers": dict(request.headers),
                "data": request.json,
                "error": "No Edit Trigger for Predictive models",
            }
            return json_response(response_data, dumps=dumps)
        
        # Proceed with further processing of the payload as needed
        # ...
        
    except Exception as e:
        logger.error(f"Error in edit_trigger: {traceback.format_exc()}")
        return json_response(
            {
                "error_message": "Internal Server Error",
                "status_code": INTERNAL_SERVER_ERROR,
                "details": str(e),
            },
            status=INTERNAL_SERVER_ERROR,
        )

@tmbrui_apis_bp.route("/upload_file", methods=["POST", "OPTIONS"], name="uploadFile")
async def upload_file(request):
    try:
        if 'file' not in request.files:
            return json_response(
                {
                    "error_message": "File not found in the request",
                    "status_code": BAD_REQUEST,
                },
                status=BAD_REQUEST,
            )

        file = request.files.get('file')
        payload = request.json
        if not payload:
            return json_response(
                {
                    "error_message": "Missing Payload Information",
                    "status_code": BAD_REQUEST,
                },
                status=BAD_REQUEST,
            )

        auth_info = payload.pop("auth", {})
        if auth_info.get("user_roles", {}).get("re_role") != "super":
            return json_response(
                {
                    "error_message": "Invalid auth information. Access denied.",
                    "status_code": UNAUTHORIZED,
                },
                status=UNAUTHORIZED,
            )

        # Process the file and insert data into the database
        df = pd.read_excel(BytesIO(file.body))
        connection = connect_db()
        cur = connection.cursor()

        original_headers = df.columns.tolist()
        cleaned_headers = [clean_header(header) for header in original_headers]

        table_name = os.getenv('TABLE_NAME', 'default_table_name')  # Get table name from env
        columns = ', '.join([f'"{header}" VARCHAR' for header in cleaned_headers])

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        );
        """

        try:
            cur.execute(create_table_query)
            connection.commit()
        except Exception as e:
            logger.error(f"Error executing create table query: {traceback.format_exc()}")
            connection.rollback()
            return json_response(
                {
                    "error_message": "Error creating table",
                    "status_code": INTERNAL_SERVER_ERROR,
                    "details": str(e),
                },
                status=INTERNAL_SERVER_ERROR,
            )

        buffer = StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        try:
            cur.copy_from(buffer, table_name, sep=',', columns=cleaned_headers)
            connection.commit()
        except Exception as e:
            logger.error(f"Error inserting data: {traceback.format_exc()}")
            connection.rollback()
            return json_response(
                {
                    "error_message": "Error inserting data",
                    "status_code": INTERNAL_SERVER_ERROR,
                    "details": str(e),
                },
                status=INTERNAL_SERVER_ERROR,
            )
        finally:
            cur.close()
            connection.close()

        return json_response({"message": "Data uploaded successfully"})

    except Exception as e:
        logger.error(f"Error in upload_file: {traceback.format_exc()}")
        return json_response(
            {
                "error_message": "Internal Server Error",
                "status_code": INTERNAL_SERVER_ERROR,
                "details": str(e),
            },
            status=INTERNAL_SERVER_ERROR,
        )

def connect_db():
    db_url = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', 5432)
    }
    return psycopg2.connect(**db_url)