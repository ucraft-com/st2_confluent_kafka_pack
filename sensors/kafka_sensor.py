from confluent_kafka import Consumer
from st2reactor.sensor.base import Sensor
import json


class KafkaSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(KafkaSensor, self).__init__(sensor_service=sensor_service, config=config)

        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = True

    def setup(self):
        conf = {
            'client.id': self.config.get("kafka_client_id"),
            'bootstrap.servers': self.config.get("kafka_bootstrap_servers"),
            'group.id': self.config.get("kafka_group_id"),
            'security.protocol': self.config.get("kafka_security_protocol"),
            'sasl.mechanism': self.config.get("kafka_sasl_mechanism"),
            'sasl.username': self.config.get("kafka_sasl_username"),
            'sasl.password': self.config.get("kafka_sasl_password"),
            'auto.offset.reset': 'earliest',
        }
        self._consumer = Consumer(conf)
        self._consumer.subscribe([self.config.get('kafka_topic')])
        self._stop = False

    def run(self):
        while not self._stop:
            msg = self._consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                pass
            else:
                value = json.loads(msg.value().decode('utf-8')) 
                key = msg.key().decode('utf-8')
                headers = { key: value.decode('utf-8') for key, value in msg.headers() }

                payload = {
                    'value': value,
                    'key': key,
                    'headers': headers
                }  

                self.sensor_service.dispatch(trigger="st2_confluent_kafka_pack.on_message", payload=payload)

    def cleanup(self):
        self._stop = True
        self._consumer.close()

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass


