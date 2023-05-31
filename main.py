#!/usr/bin/env python3
import frontend
import networkx as nx
from matplotlib import pyplot as plt
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
    @ui.page('/graph')
    def some_graph():

        with ui.pyplot(figsize=(10, 5)):
                    
                    G = nx.Graph()
                    G.add_edge(1, 2)
                    G.add_edge(1, 3)
                    G.add_edge(1, 5)
                    G.add_edge(2, 3)
                    G.add_edge(3, 4)
                    G.add_edge(4, 5)

                    # explicitly set positions
                    pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}

                    options = {
                        "font_size": 36,
                        "node_size": 3000,
                        "node_color": "white",
                        "edgecolors": "black",
                        "linewidths": 5,
                        "width": 5,
                    }
                    nx.draw_networkx(G, pos, **options)

                    # Set margins for the axes so that nodes aren't clipped
                    ax = plt.gca()
                    ax.margins(0.20)
                    plt.axis("off")
            

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
