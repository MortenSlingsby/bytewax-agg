import json
import random
import ast

from datetime import datetime, timedelta, timezone

from bytewax.dataflow import Dataflow
from bytewax.inputs import KafkaInputConfig
from bytewax.outputs import ManualOutputConfig
from bytewax.execution import run_main, PeriodicEpochConfig
from bytewax.window import SystemClockConfig, TumblingWindowConfig
from bytewax.recovery import KafkaRecoveryConfig

id_columns = ["id"]

KAFKA_CONFIG={
  "brokers": ["localhost:19092"],
  "topic": "bytewax-dummy",
  "tail": True,
  "starting_offset": "beginning",
  "additional_properties": {}
}

recovery_config = KafkaRecoveryConfig(["localhost:19092"], "recovery")

def get_value(data):
    key, value = data
    raw = json.loads(value.decode())
    return raw

def output_row(data):
    return data

def split(data):
    identifier = {k: data[k] for k in ('start','type')}
    return str(identifier), data

def reducer(accumulator, value):
    accumulator["quantity"] = accumulator["quantity"] + value["quantity"]
    accumulator["price"] = accumulator["price"] + value["price"]
    return accumulator


def build_count_new():
    state = { "quantity": 0, "price": 0 }
    return state

def agg(state, value):
    state["quantity"] = state["quantity"] + value["quantity"]
    state["price"] = state["price"] + value["price"]
    return state, state

def out(data):
    key, value = data
    total = ast.literal_eval(key) | value
    total["start"] = datetime.fromtimestamp(total["start"], timezone.utc).strftime("%Y-%m-%dT%H:%M")
    total["quantity"] = round(total["quantity"],1)
    total["price"] = round(total["price"],2)
    return total

def output_builder(worker_index,worker_count):
    def write_to_api(data):
        # count = random.choice([1,5,7])
        # print(count)
        # if count == 1:
        #     raise Exception
        print(data)
    return write_to_api

clock_config = SystemClockConfig()
window_config = TumblingWindowConfig(length=timedelta(seconds=10),)

flow = Dataflow()
flow.input("input", KafkaInputConfig(**KAFKA_CONFIG))


flow.map(get_value)
flow.flat_map(output_row)
flow.map(split)

# Reduce and aggregate
flow.reduce_window("count", clock_config, window_config, reducer)
flow.stateful_map("aggr", build_count_new, agg)

# Prep and send output
flow.map(out)

# flow.map(write_to_api)
flow.capture(ManualOutputConfig(output_builder))

run_main(flow, recovery_config=recovery_config, epoch_config=PeriodicEpochConfig(timedelta(seconds=10)))
