from confluent_kafka import Consumer
from st2reactor.sensor.base import Sensor

import re
import json
import datetime


class KafkaSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(KafkaSensor, self).__init__(sensor_service=sensor_service, config=config)

        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = True
        self._topics = []
        self._topic_tiggers = {}

    def setup(self):
        conf = {
            "client.id": self.config.get("kafka_client_id"),
            "bootstrap.servers": self.config.get("kafka_bootstrap_servers"),
            "group.id": self.config.get("kafka_group_id"),
            "security.protocol": self.config.get("kafka_security_protocol"),
            "sasl.mechanism": self.config.get("kafka_sasl_mechanism"),
            "sasl.username": self.config.get("kafka_sasl_username"),
            "sasl.password": self.config.get("kafka_sasl_password"),
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
        }
        self._consumer = Consumer(conf)
        self.config_topic_convertor()
        self.subscribe_to_topics()
        self._logger.info("Kafka Sensor Setup")

    def run(self):
        while not self._stop:
            msg = self._consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                pass
            else:
                try:
                    value = json.loads(msg.value().decode("utf-8"))
                    key = msg.key().decode("utf-8") if msg.key() is not None else None
                    headers = (
                        {key: value.decode("utf-8") for key, value in msg.headers()}
                        if msg.headers() is not None
                        else None
                    )
                    topic_name = msg.topic()

                    if self.config.get("timestamp"):
                        value["timestamp"] = self.calculate_timestamp(value)

                    payload = {"value": value, "key": key, "headers": headers}

                    triggers = self._topic_tiggers[topic_name]

                    # Note: The email ("automationucraft@gmail.com") statement work only for stage!
                    for trigger in triggers:
                        email = (
                            payload.get("value", {})
                            .get("context", {})
                            .get("user", {})
                            .get("email", "")
                        )

                        # List of static excluded emails
                        excluded_emails = [
                            "automationucraft@gmail.com",
                            "harut.k.petrosyan@gmail.com",
                            "ucraftbackupuser@gmail.com",
                            "narinebettest+111888@gmail.com",
                            "margarit.sh@ucraft.com",
                            "satine+999@ucraft.com",
                            "qaucraft@gmail.com",
                            "elianora123@yahoo.com",
                            "userucraft@gmail.com",
                            "ucraft.templates@gmail.com",
                        ]

                        # Check if the email is in the excluded list or matches the dynamic pattern
                        if (
                            email not in excluded_emails
                            # and not re.match(r"testers\+.*@ucraft\.com", email)
                            # and not re.match(r"BillingUser-\w+@ucraft\.billing", email)
                        ):
                            self.sensor_service.dispatch(
                                trigger=trigger, payload=payload
                            )

                except Exception as e:
                    self._logger.info(str(e))
                    self._logger.info("Message Faild")

                self._consumer.commit(message=msg)

    def cleanup(self):
        self._stop = True
        self._consumer.close()

    def config_topic_convertor(self):
        config_topic = self.config.get("kafka_topic")
        configs = config_topic.split(",")

        for config in configs:
            topic = config.split(":")[0].strip()
            self._topics.append(topic)

            triggers = config.split(":")[1].split(" ")
            self._topic_tiggers[topic] = []

            for trigger in triggers:
                self._topic_tiggers[topic].append(trigger)

        self._logger.info("Topic Configure")

    def subscribe_to_topics(self):
        topics = self._topics

        if topics:
            self._consumer.subscribe(topics)
            self._stop = False
            self._logger.info("Subscribe To Topic")
        else:
            self._consumer.unsubscribe()
            self._stop = True
            self._logger.info("Unsubscribe To Topic")

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def calculate_timestamp(self, value):
        context = value.get("context", {})
        receivedAt = datetime.datetime.now().timestamp()
        newMs = receivedAt

        if "originalTimestamp" in context and "sentAt" in context:
            newMs = receivedAt - (context["sentAt"] - context["originalTimestamp"])

        timestempM = datetime.datetime.fromtimestamp(newMs)

        return str(timestempM)
