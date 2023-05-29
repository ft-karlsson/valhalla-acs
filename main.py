#!/usr/bin/env python3
import frontend
from fastapi import FastAPI
from kafka import KafkaConsumer
import datamodel
import threading
import json

from nicegui import ui

app = FastAPI()

# def consumer(somedict):

#     try:
#         # To consume latest messages and auto-commit offsets
#         consumer = KafkaConsumer('acs_subscribers',
#                                 #  group_id='acs2',
#                                  bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')
#         for message in consumer:
#             # message value and key are raw bytes -- decode if necessary!
#             # e.g., for unicode: `message.value.decode('utf-8')`
#             print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
#                                                  message.offset, message.key,
#                                                  message.value))
#             some_key = message.key.decode('utf-8')
#             some_data = message.value.decode('utf-8')
#             d = json.loads(some_data)
#             somedict.update({some_key: d})
#     except Exception as e:
#         print("Error!!", e)


@app.on_event("startup")
def run_subscriber_topic():
    datamodel.subscribers


def init(app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        # first = datamodel.subscribers('su0112330')['subscriber_id']
        with ui.tabs() as tabs:
            ui.tab('Home', icon='home')
            ui.tab('About', icon='info')
            ui.tab('Devices', icon='router')
            ui.tab('Subscribers', icon='people')

        with ui.tab_panels(tabs, value='Home'):
            with ui.tab_panel('Home'):
                ui.label('This is the first tab')
            with ui.tab_panel('About'):
                ui.label('This is the second tab')
            with ui.tab_panel('Devices'):
                ui.label('This is the devices tab')
            with ui.tab_panel('Devices'):
                ui.label('This is the devices tab')
            with ui.tab_panel('Subscribers'):
                ui.label('This is the subscriber tab')
                with ui.grid(columns=2):
                    ui.label('Name:')
                    sub = datamodel.subscribers['su0112330']['subscriber_id']
                    ui.label(sub)

                    ui.label('products:')
                    label = ui.label()
                    ui.timer(1.0, lambda: label.set_text(datamodel.subscribers['su0112330']['products'][0]['product_id']))

                    ui.label('Height:')
                    ui.label('1.80m')

    ui.run_with(app)



@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/test')
def show_dict():
    return {datamodel.subscribers}

init(app)

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
