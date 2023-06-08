import asyncio
import json
import os
import logging

logger = logging.getLogger(__name__)

from aiokafka import AIOKafkaConsumer

# Environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Global variables
sub_loop = asyncio.get_event_loop()
dev_loop = asyncio.get_event_loop()
dp_loop = asyncio.get_event_loop()

consumer1 = AIOKafkaConsumer("acs_subscribers", loop=sub_loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
consumer2 = AIOKafkaConsumer("acs_devices", loop=dev_loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
consumer3 = AIOKafkaConsumer("acs_device_policies", loop=dev_loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')


class ThreadSafeDictionary:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._dictionary = {}

    def __getitem__(self, key):
        return self._dictionary[key]

    def __setitem__(self, key, value):
        self._dictionary[key] = value

    def __delitem__(self, key):
        del self._dictionary[key]

    def __len__(self):
        return len(self._dictionary)

    def keys(self):
        return self._dictionary.keys()

    def values(self):
        return self._dictionary.values()

    def items(self):
        return self._dictionary.items()


async def consume_from_kafka(consumer, dictionary, topic):
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            some_key = msg.key.decode('utf-8')
            some_data = msg.value.decode('utf-8')
            print(f"Got new message for topic '{topic}' with key: {some_key}")
            try:
                d = json.loads(some_data)
                async with dictionary._lock:
                    dictionary._dictionary[some_key] = d
            except json.JSONDecodeError as e:
                print(f"Decode error on message with key: {some_key}: {e}")
    finally:
        await consumer.stop()


import aiokafka

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


# Create instances of the thread-safe dictionary
subscribers = ThreadSafeDictionary()
devices = ThreadSafeDictionary()
policies = ThreadSafeDictionary()


# Start consuming messages from Kafka and update the dictionaries
sub_loop.create_task(consume_from_kafka(consumer1, subscribers, "acs_subscribers"))
dev_loop.create_task(consume_from_kafka(consumer2, devices, "acs_devices"))
dp_loop.create_task(consume_from_kafka(consumer3, policies, "acs_device_policies"))
