# Bytewax state recovery issue.

To reproduce follow these steps. If using nix, start by running `nix develop`, otherwise make sure you got the required packages available and just ignore the .nix files. Packages used:
- bytewax
- Kafka-python

## 1. Create local redpanda instance
The redpanda broker can be reached on `localhost:19092`. Run the below to start a local cluster
```
docker compose -f redpanda/docker-compose.yaml up -d
```
To open the redpanda console, open `localhost:8080`. You can easily delete your topics here in case you want to reset the recovery or input topics.

## 2. Fill topic with dummy data
We create a topic called `bytewax-dummy` by running:
```
python fill_topic.py
```

## 3. Start dataflow
Open a new terminal window and run:
```
python consume_bytewax.py
```

## 4. Add new rows and monitor resulting aggregate
In the previous terminal, we add 5 new rows by running:
```
python producer_new.py
```
With each run of this script you can check the output in the dataflow terminal. The quantity should increase with 100 and the price with 500 for the rows with key `start: '2022-01-01T13:00` and `type: BUY`

## 5. Recreate error
The easiest way to recreate the issue is by running the below steps. Note that the error does not occur always, so you might need repeat these steps several times until you encounter the error
- Run `python redpanda/produce_new.py`
- Wait for output terminal windows to produce result
- Immediatly stop the dataflow with using ctrl-z
- Restart the dataflow by running `python consume_bytewax.py`

On occasion the output does not provide the latest aggregated result. When you then continue adding new data the program starts aggregating from this incorrect state, thus effectively leading to data loss.



