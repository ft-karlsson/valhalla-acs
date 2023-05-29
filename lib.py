import threading
from kafka import KafkaConsumer
import json
import time

class ThreadSafeDictionary:
    def __init__(self, topic, bootstrap_servers, auto_offset_reset='earliest'):
        self._lock = threading.Lock()
        self._dictionary = {}
        self._consumer_thread = threading.Thread(target=self._consume_from_kafka, args=(topic, bootstrap_servers, auto_offset_reset))
        self._consumer_thread.start()

    def __getitem__(self, key):
        with self._lock:
            return self._dictionary[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._dictionary[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._dictionary[key]

    def __len__(self):
        with self._lock:
            return len(self._dictionary)

    def keys(self):
        with self._lock:
            return self._dictionary.keys()

    def values(self):
        with self._lock:
            return self._dictionary.values()

    def items(self):
        with self._lock:
            return self._dictionary.items()

    def _consume_from_kafka(self, topic, bootstrap_servers, auto_offset_reset='earliest'):
        consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, auto_offset_reset=auto_offset_reset)
        for message in consumer:
            some_key = message.key.decode('utf-8')
            some_data = message.value.decode('utf-8')
            print(f"got new msg with key: {some_key}")
            d = json.loads(some_data)
            with self._lock:
                self._dictionary.update({some_key: d})
