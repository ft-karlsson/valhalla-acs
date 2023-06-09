import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer

logger = logging.getLogger(__name__)

class DataModelBuilder:
    def __init__(self, kafka_bootstrap_servers, topic):
        self.KAFKA_BOOTSTRAP_SERVERS = kafka_bootstrap_servers
        self.topic = topic
        self.consumer = None
        self.dictionary = None

    def create_consumer(self, loop):
        consumer = AIOKafkaConsumer(self.topic, loop=loop, bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS, auto_offset_reset='earliest')
        return consumer

    def create_thread_safe_dictionary(self):
        return ThreadSafeDictionary()

    async def consume_from_kafka(self, consumer, dictionary):
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                some_key = msg.key.decode('utf-8')
                some_data = msg.value.decode('utf-8')
                print(f"Got new message for topic '{self.topic}' with key: {some_key}")
                try:
                    d = json.loads(some_data)
                    async with dictionary._lock:
                        dictionary._dictionary[some_key] = d
                except json.JSONDecodeError as e:
                    print(f"Decode error on message with key: {some_key}: {e}")
        finally:
            await consumer.stop()

    def build(self):
        self.consumer = self.create_consumer(asyncio.get_event_loop())
        self.dictionary = self.create_thread_safe_dictionary()

        asyncio.get_event_loop().create_task(self.consume_from_kafka(self.consumer, self.dictionary))

        return self.dictionary

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

subscribers = DataModelBuilder("localhost:9092", "acs_subscribers").build()
devices = DataModelBuilder("localhost:9092", "acs_devices").build()
policies = DataModelBuilder("localhost:9092", "acs_device_policies").build()
