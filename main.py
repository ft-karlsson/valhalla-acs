from random import randint
from fastapi import FastAPI, Body, HTTPException
from fastapi.logger import logger
import uvicorn
import frontend
import datamodel
from nicegui import ui
from typing import Union


from cwmp_lib.soap import parse_inform
# Instantiate the API
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# TODO: rm this (for debugging data)
@app.get("/subscribers")
async def get_subscribers():
    return dict(datamodel.subscribers.items())

# TODO: rm this (for debugging data)
@app.get("/devices")
async def get_subscribers():
    return dict(datamodel.devices.items())

@app.post("/deviceapi")
def read_inform(inform_msg: str = Body(...)):
    try:
        inform = parse_inform(inform_msg)
    except Exception:
        raise HTTPException(status_code=400, detail="could not parse soap event")

    return {"msg": inform}

frontend.init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
