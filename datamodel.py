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
consumer1 = AIOKafkaConsumer("acs_subscribers", loop=sub_loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
consumer2 = AIOKafkaConsumer("acs_devices", loop=dev_loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')


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


async def consume_from_kafka_subscriber(subscribers):
    await consumer1.start()
    try:
        # Consume messages
        async for msg in consumer1:
            some_key = msg.key.decode('utf-8')
            some_data = msg.value.decode('utf-8')
            logger.info(f"Got new sub message with key: {some_key}")
            d = json.loads(some_data)
            async with subscribers._lock:
                subscribers._dictionary[some_key] = d
    finally:
        await consumer1.stop()

async def consume_from_kafka_devices(devices):
    await consumer2.start()
    try:
        # Consume messages
        async for msg in consumer2:
            some_key = msg.key.decode('utf-8')
            some_data = msg.value.decode('utf-8')
            logger.info(f"Got new device message with key: {some_key}")
            d = json.loads(some_data)
            async with devices._lock:
                devices._dictionary[some_key] = d
    finally:
        await consumer2.stop()


# Create an instance of the thread-safe dictionary
subscribers = ThreadSafeDictionary()

devices = ThreadSafeDictionary()

# Start consuming messages from Kafka and update the dictionary
sub_loop.create_task(consume_from_kafka_subscriber(subscribers))
dev_loop.create_task(consume_from_kafka_devices(devices))
