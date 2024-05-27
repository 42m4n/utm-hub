import logging
import time

import pika
import sys

from conf import RabbitMQ


class RabbitMQHandler(logging.Handler):

    def __init__(self, host=RabbitMQ.host, port=RabbitMQ.port, exchange=RabbitMQ.exchange,
                 routing_key=RabbitMQ.routing_key, queue_name=RabbitMQ.queue_name):

        super().__init__()
        self.host = host
        self.port = port
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        while True:

            try:
                credentials = pika.PlainCredentials(username=RabbitMQ.username, password=RabbitMQ.password)

                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials, heartbeat=600))
                self.channel = self.connection.channel()

                # check if queue exists in rabbitmq
                queue_declare_ok = self.channel.queue_declare(queue=self.queue_name, durable=False, passive=True)
                if not queue_declare_ok.method.queue:
                    self.channel.queue_declare(queue=self.queue_name,
                                               durable=False)

                # Check if the exchange exists
                exchange_declare_ok = self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct',
                                                                    passive=True)
                if not exchange_declare_ok:
                    self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

                self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=self.routing_key)

                break
            except pika.exceptions.StreamLostError:
                print("Connection to Rabbitmq lost. Reconnecting...")
                logger.warning("Connection to Rabbitmq lost. Reconnecting...")
                time.sleep(1)

    def emit(self, record):
        if not self.connection or self.connection.is_closed:
            self.connect()
        message = self.format(record)
        formatted_message = f"{record.asctime} | {record.filename} | {record.levelname} | {message}"

        self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=formatted_message)

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()


logger = logging.getLogger()

formatter = logging.Formatter('%(asctime)s | %(filename)s | %(levelname)s | %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

rabbitmq_handler = RabbitMQHandler()
logger.addHandler(console_handler)
logger.addHandler(rabbitmq_handler)

logger.setLevel(logging.INFO)
