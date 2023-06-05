from random import randint
from fastapi import FastAPI
from fastapi.logger import logger
import uvicorn
import frontend
import datamodel
from nicegui import ui

# Instantiate the API
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/subscribers")
async def get_subscribers():
    return dict(datamodel.subscribers.items())
@app.get("/devices")
async def get_subscribers():
    return dict(datamodel.devices.items())

frontend.init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
