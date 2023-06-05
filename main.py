from random import randint
from fastapi import FastAPI
import uvicorn
import frontend
import datamodel
from nicegui import ui
# Instantiate the API
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await datamodel.consumer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await datamodel.consumer.stop()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/subscribers")
async def get_subscribers():
    return dict(datamodel.subscribers.items())

frontend.init(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
