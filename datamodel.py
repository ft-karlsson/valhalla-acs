import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

# Environment variables
KAFKA_TOPIC = "acs_subscribers"
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Global variables
loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')


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


async def consume_from_kafka(topic, dictionary):
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            some_key = msg.key.decode('utf-8')
            some_data = msg.value.decode('utf-8')
            print(f"Got new message with key: {some_key}")
            d = json.loads(some_data)
            async with dictionary._lock:
                dictionary._dictionary[some_key] = d
    finally:
        await consumer.stop()


# Create an instance of the thread-safe dictionary
subscribers = ThreadSafeDictionary()

# Start consuming messages from Kafka and update the dictionary
loop.create_task(consume_from_kafka(KAFKA_TOPIC, subscribers))
