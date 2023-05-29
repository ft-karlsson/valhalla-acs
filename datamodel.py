import threading
from lib import ThreadSafeDictionary
import time

# Create an instance of the thread-safe dictionary with Kafka consumer
subscribers = ThreadSafeDictionary('acs_subscribers', ['localhost:9092'])

# Create another instance of the thread-safe dictionary with Kafka consumer
# devices = ThreadSafeDictionary('acs_devices', ['localhost:9092'])

# Function to print the dictionary items
# def print_items():
#     while True:
#         items = somedict.items()
#         print(items)
#         time.sleep(2)
#         # Add sleep or other logic here if needed

# # Create a thread to print the dictionary items
# print_thread = threading.Thread(target=print_items)
# print_thread.start()

# # Wait for threads to finish
# print_thread.join()
