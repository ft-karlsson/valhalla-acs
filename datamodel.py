import threading
from model_lib import ThreadSafeDictionary
import time

# Create an instance of the thread-safe dictionary with Kafka consumer
subscribers = ThreadSafeDictionary('acs_subscribers', ['localhost:9092'])

# Create another instance of the thread-safe dictionary with Kafka consumer
graphtest = ThreadSafeDictionary('graph_test', ['localhost:9092'])

