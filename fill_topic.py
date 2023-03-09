import time
import random
import json
import math
import datetime
import logging

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

BROKER = 'localhost:19092'
TOPIC_NAME = "bytewax-dummy"

KAFKA_CONFIG = {
  "bootstrap_servers": BROKER,
}
admin = KafkaAdminClient(**KAFKA_CONFIG)
try:
    logging.info(f"Create topic {TOPIC_NAME} if not exist")
    admin.create_topics(new_topics=[
        NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)])
except TopicAlreadyExistsError as e:
    logging.info(f"Topic {TOPIC_NAME} already exsist")

def round_up(num):
    return math.ceil(num / 10) * 10

logging.info("Start producing")

p = KafkaProducer(**KAFKA_CONFIG, acks="all")

start_date = datetime.datetime(2022, 1, 1, 12, 00, 00)

for i in range(1,100):
    start = start_date + datetime.timedelta(hours = random.choice([1,2,3]))
    new_data = [{
        "type":random.choice(["BUY", "SELL"]),
        "price":round_up(random.choice(range(0,1000))),
        "quantity":round_up(random.choice(range(0,100))),
        "start":round(start.timestamp()),
        "id":random.choice(range(0,10000))
    }]

    out = json.dumps(new_data).encode()
    f = p.send(TOPIC_NAME, out)
p.close()

logging.info("Finish producing")

