import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer

logger = logging.getLogger(__name__)


"""
datamodel
~~~~~~~~~~~~~~~~~
This module contains the classes that define our datamodels used for the ACS server
"""


class DataModelBuilder:
    """DataModelBuilder class will create and async consumer tasks based on a givin kafka topic,
    and keep it in sync with threadsafe dictionary type, the class instances itself can be used
    just like a python dictionary for easy integration with frontend.
    """

    def __init__(self, kafka_bootstrap_servers, topic, validator_func=None):
        self.KAFKA_BOOTSTRAP_SERVERS = kafka_bootstrap_servers
        self.topic = topic
        self.consumer = None
        self.dictionary = None
        self.validator_func = validator_func

    def create_consumer(self, loop):
        consumer = AIOKafkaConsumer(
            self.topic,
            loop=loop,
            bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",
        )
        return consumer

    def create_thread_safe_dictionary(self):
        return ThreadSafeDictionary()

    async def consume_from_kafka(self, consumer, dictionary):
        await consumer.start()
        try:
            # Consume messages
            async for msg in consumer:
                some_key = msg.key.decode("utf-8")
                some_data = msg.value.decode("utf-8")
                print(f"Got new message for topic '{self.topic}' with key: {some_key}")
                try:
                    d = json.loads(some_data)
                    if self.validator_func is not None:
                        try:
                            self.validator_func(d)  # Call the decorated validator function
                        except ValueError:
                            print("skipping")
                            continue  # Skip the message if validation fails
                    async with dictionary._lock:
                        dictionary._dictionary[some_key] = d
                except json.JSONDecodeError as e:
                    print(f"Decode error on message with key: {some_key}: {e}")
        finally:
            await consumer.stop()

    def build(self):
        self.consumer = self.create_consumer(asyncio.get_event_loop())
        self.dictionary = self.create_thread_safe_dictionary()

        asyncio.get_event_loop().create_task(
            self.consume_from_kafka(self.consumer, self.dictionary)
        )

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

# here define a custom decorator logging 
def validate_logger(validator_func):
    def decorator(data):
        try:
            validator_func(data)
        except ValueError as e:
            print(f"Validation error: {e}")
            raise ValueError
    return decorator

# Here are the specific validators using the decorator
@validate_logger
def device_validator(data):
    if "manufacturer" not in data:
        raise ValueError("missing 'manufacturer' field")
    # TODO: add more validation


@validate_logger
def subscriber_validator(data):
    if "serialnumber" not in data:
        raise ValueError("missing 'serialnumber' field")


@validate_logger
def policy_validator(data):
    pass


# Instantiation of each part of the datamodel
devices = DataModelBuilder("localhost:9092", "acs_devices", device_validator).build()
subscribers = DataModelBuilder("localhost:9092", "acs_subscribers", subscriber_validator).build()
policies = DataModelBuilder("localhost:9092", "acs_device_policies").build()
