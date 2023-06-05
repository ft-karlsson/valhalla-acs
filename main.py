#!/usr/bin/env python3
import frontend
import networkx as nx
from matplotlib import pyplot as plt
from fastapi import FastAPI
import datamodel

from nicegui import ui

app = FastAPI()


@app.on_event("startup")
def run_subscriber_topic():
    datamodel.subscribers


@app.get('/')
def read_root():
    return {'Hello': 'World'}

# TODO: FOR TEST. REMOVE THIS!!
@app.get('/test')
def show_dict():
    return {datamodel.subscribers}

frontend.init(app)

if __name__ == '__main__':
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
