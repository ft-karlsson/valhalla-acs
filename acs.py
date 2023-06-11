"""
acs
~~~~~~~~~~~~~~~~~
This module contains specific functions specific to "auto-configuration of devices"
"""


async def send_kafka_message(topic, data, key):
    ## TODO: Want to make the producer global when under production load so not to create producer instances on every request
    producer = aiokafka.AIOKafkaProducer(bootstrap_servers="localhost:9092", client_id="acs-server")
    await producer.start()
    encoded_key = key.encode('utf-8')
    encoded_value = json.dumps(data).encode('utf-8')
    try:
        d = json.dumps(data)
    except TypeError:
        print("could not parse to valid json")
    try:
        await producer.send_and_wait(topic,encoded_value, encoded_key)
    except Exception as e:
        raise Exception(f"could not produce message due to: {e}")

    finally:
        await producer.stop()


async def ingest_device(parsed_inform: dict) -> bool:
    # TODO: do some validation of data keys
    parsed_inform['serialnumber']
    await send_kafka_message("acs_devices", parsed_inform, parsed_inform['serialnumber'])
