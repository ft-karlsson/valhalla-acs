from random import randint
from fastapi import FastAPI, Body, HTTPException
from fastapi.logger import logger
import uvicorn
import frontend
import datamodel
from nicegui import ui
from typing import Union

from cwmp_lib.soap import parse_inform
from acs import ingest_device

# Instantiate the API
app = FastAPI()

# TODO: rm this (for debugging data)
@app.get("/subscribers")
async def get_subscribers():
    return dict(datamodel.subscribers.items())

# TODO: rm this (for debugging data)
@app.get("/devices")
async def get_subscribers():
    return dict(datamodel.devices.items())

@app.post("/deviceapi")
async def read_inform(inform_msg: str = Body(...)):
    """ Parse and ingest the device on bootup """
    try:
        inform = parse_inform(inform_msg)
        await ingest_device(inform)
    except Exception:
        raise HTTPException(status_code=400, detail="could not parse soap event")

    # TODO: should just return 200 
    return {"msg": inform}

frontend.init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
