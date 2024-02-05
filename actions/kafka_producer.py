from st2common.runners.base_action import Action
from confluent_kafka import Producer
import json

class KafkaProducer(Action):
    def run(self, topic, message, key=None, headers=None, partitioner=None):
        try:
            conf = {
                'client.id': self.config.get("kafka_client_id"),
                'bootstrap.servers': self.config.get("kafka_bootstrap_servers"),
                'security.protocol': self.config.get("kafka_security_protocol"),
                'sasl.mechanism': self.config.get("kafka_sasl_mechanism"),
                'sasl.username': self.config.get("kafka_sasl_username"),
                'sasl.password': self.config.get("kafka_sasl_password"),
                'partitioner': str(partitioner),
            }
            producer = Producer(conf)
            json_msg = json.loads(message)
            producer.produce(topic, value=json.dumps(json_msg).encode('utf-8'), key=key, headers=headers)
            producer.flush()

        except Exception as e:
            return f"Error: {str(e)}"

