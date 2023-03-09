import time
import random
import json
import logging

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

BROKER = 'localhost:19092'
TOPIC_NAME = "bytewax-dummy"

KAFKA_CONFIG = {
  "bootstrap_servers": BROKER,
}

logging.info("Start producing")

p = KafkaProducer(**KAFKA_CONFIG, acks="all")

for i in range(1,6):
    new_data = [{
        "type":"BUY",
        "price":100,
        "quantity":20,
        "start":1641042000,
        "id":random.choice(range(0,10000))
    }]

    out = json.dumps(new_data).encode()
    f = p.send(TOPIC_NAME, out)
p.close()

logging.info("Finish producing")

