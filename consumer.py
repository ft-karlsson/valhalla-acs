from kafka import KafkaConsumer
import multiprocessing
import threading
import time
import json

def run_subscriber_topic(somedict):
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer('acs_subscribers',
                                #  group_id='acs2',
                                 bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
        for message in consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            #                                      message.offset, message.key,
            #                                      message.value))
            some_key = message.key.decode('utf-8')
            some_data = message.value.decode('utf-8')
            d = json.loads(some_data)
            somedict.update({some_key: d})
    except Exception as e:
        print("Error!!", e)


def check_data(some_dict):
    while True:
        time.sleep(2)
        print("sub_memory: " + str(len(some_dict)))
        print(some_dict)


if __name__ == "__main__":
    sub_dictionary = {}
    x1 = threading.Thread(target=check_data, args=(sub_dictionary,))
    x2 = threading.Thread(target=run_subscriber_topic, args=(sub_dictionary,))
    x1.start()
    x2.start()
    # x1.join()


# import multiprocessing
# import time
# def add():
#         try:
#         # To consume latest messages and auto-commit offsets
#             consumer = KafkaConsumer('acs_subscribers_2',
#                                     group_id='acs',
#                                     bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
#             for message in consumer:
#                 # message value and key are raw bytes -- decode if necessary!
#                 # e.g., for unicode: `message.value.decode('utf-8')`
#                 print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                                     message.offset, message.key,
#                                                     message.value))
#                 # sub_dictionary.update({"subscriber_id": message.value})
#         except:
#             print("Error!!")

# import threading, queue

# q = queue.Queue()

# def worker():
#     while True:
#         message = q.get()
#         print(f'Working on {message}')
#         ''' Do the processing on messages '''
#         print(f'Finished {message}')
#         q.task_done()

# # spawn some threads to run worker
# threading.Thread(target=worker, daemon=True).start()


# #function to read from kafka
# def f():
#     consumer = KafkaConsumer('acs_subscribers',
#                                     group_id='acs',
#                                     bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
#     for message in consumer:
#         q.put(message)

# #Either run the function f directly or allocate some thread to run it
# f()
# # Alter: threading.Thread(target=f, daemon=True).start()

# print('All task requests sent\n', end='')
# # block until all tasks are done
# q.join()
# print('All work completed')
