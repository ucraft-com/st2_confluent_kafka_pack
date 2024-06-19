import json

from confluent_kafka import Producer

from st2common.runners.base_action import Action


class KafkaProducer(Action):
    def run(self, topic, message, key=None, headers=None, partitioner=None):
        try:
            # Kafka configuration parameters
            conf = {
                "client.id": self.config.get("kafka_client_id"),
                "bootstrap.servers": self.config.get("kafka_bootstrap_servers"),
                "security.protocol": self.config.get("kafka_security_protocol"),
                "sasl.mechanism": self.config.get("kafka_sasl_mechanism"),
                "sasl.username": self.config.get("kafka_sasl_username"),
                "sasl.password": self.config.get("kafka_sasl_password"),
                "partitioner": str(partitioner),
            }

            # Create Kafka producer with the provided configuration
            producer = Producer(conf)

            # Parse the incoming message as JSON
            json_msg = json.loads(message)

            # Produce the message to the specified topic
            producer.produce(
                topic,
                value=json.dumps(json_msg).encode("utf-8"),
                key=key,
                headers=headers,
            )

            # Flush the producer to ensure all messages are sent
            producer.flush()

            # Return success message
            return {"message": "Data has been produced successfully", "data": json_msg}
        except Exception as e:
            # If an exception occurs during production, return error message
            return {"message": f"Error Kafka producer: {str(e)}", "data": json_msg}
