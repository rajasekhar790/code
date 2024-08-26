from confluent_kafka import Consumer, KafkaError
from microservice.capabilities.config_variables import (
    KAFKA_SERVER,
    KAFKA_CERT,
    KAFKA_CERT_PASSWORD,
    TOPIC_DICT,
)
import json

def process_message(message):
    """
    Process the message received from Kafka.
    This is a placeholder function that you would replace with your actual processing logic.
    """
    print(f"Received message: {message}")

def kafka_message_consumer(topic_key):
    try:
        config = {
            "bootstrap.servers": KAFKA_SERVER,
            "security.protocol": "SSL",
            "ssl.certificate.location": KAFKA_CERT,
            "ssl.ca.location": KAFKA_CERT,
            "ssl.key.location": KAFKA_CERT,
            "ssl.key.password": KAFKA_CERT_PASSWORD,
            "group.id": "your_consumer_group",  # Replace with your consumer group
            "auto.offset.reset": "earliest",  # or "latest"
        }

        kafka_consumer = Consumer(**config)
        topic_name = TOPIC_DICT[topic_key]

        # Subscribe to the topic
        kafka_consumer.subscribe([topic_name])

        print(f"Subscribed to topic: {topic_name}")

        while True:
            msg = kafka_consumer.poll(timeout=1.0)

            if msg is None:
                continue  # No message, continue polling
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"Reached end of partition: {msg.topic()}[{msg.partition()}] at offset {msg.offset()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Message is valid
                message = json.loads(msg.value().decode('utf-8'))
                process_message(message)

    except Exception as ex:
        print(f"Error in Kafka consumer: {str(ex)}")
    finally:
        kafka_consumer.close()

if __name__ == "__main__":
    # Example usage
    kafka_message_consumer("your_topic_key")  # Replace with your actual topic key