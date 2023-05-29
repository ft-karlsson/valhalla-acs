from fastapi import FastAPI

from nicegui import ui

## is to be the front-end part using nicegui
def init(app: FastAPI) -> None:
    @ui.page('/show')
    def show():

        ui.label("hello from nicegui")

    ui.run_with(app)
