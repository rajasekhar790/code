SELECT
    SUM(CASE WHEN 'Admin' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Admin",
    SUM(CASE WHEN 'Super Admin' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Super Admin",
    SUM(CASE WHEN 'Manager' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Manager",
    SUM(CASE WHEN 'Viewers' = ANY(string_to_array(Roles, ',')) THEN 1 ELSE 0 END) AS "Viewers"
FROM user_details;


SELECT
    SUM(CASE WHEN 'Admin' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Admin",
    SUM(CASE WHEN 'Super Admin' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Super Admin",
    SUM(CASE WHEN 'Manager' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Manager",
    SUM(CASE WHEN 'Viewers' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Viewers"
FROM user_details;

SELECT
    SUM(CASE WHEN 'Admin' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Admin",
    SUM(CASE WHEN 'Super Admin' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Super Admin",
    SUM(CASE WHEN 'Manager' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Manager",
    SUM(CASE WHEN 'Viewers' = ANY(ARRAY(SELECT jsonb_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Viewers"
FROM user_details;


SELECT
    SUM(CASE WHEN 'Admin' = ANY(ARRAY(SELECT json_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Admin",
    SUM(CASE WHEN 'Super Admin' = ANY(ARRAY(SELECT json_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Super Admin",
    SUM(CASE WHEN 'Manager' = ANY(ARRAY(SELECT json_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Manager",
    SUM(CASE WHEN 'Viewers' = ANY(ARRAY(SELECT json_array_elements_text(Roles))) THEN 1 ELSE 0 END) AS "Viewers"
FROM user_details;