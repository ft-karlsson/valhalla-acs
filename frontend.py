from fastapi import FastAPI
import networkx as nx
from matplotlib import pyplot as plt
import datamodel
from nicegui import ui

## is to be the front-end part using nicegui
def init(app: FastAPI) -> None:
    @ui.page('/show')
    def show():
        # first = datamodel.subscribers('su0112330')['subscriber_id']
        with ui.tabs() as tabs:
            ui.tab('Home', icon='home')
            ui.tab('About', icon='info')
            ui.tab('Devices', icon='router')
            ui.tab('Subscribers', icon='people')
            ui.tab('Policies', icon='poll')

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
                    sub = datamodel.subscribers['su0112330']['first_name']
                    ui.label(sub)

                    ui.label('products:')
                    product = ui.label()
                    ui.timer(1.0, lambda: product.set_text(datamodel.subscribers['su0112330']['products'][0]['product_id']))
                    
                    ui.label('model:')
                    model = ui.label()
                    ui.timer(1.0, lambda: model.set_text(datamodel.devices['su0112330']['model']))
            with ui.tab_panel('Policies'):
                ui.label('This is the policies tab')
                    
    @ui.page('/graph')
    def some_graph():
        with ui.pyplot(figsize=(10, 5)):
            edges = [('lvl-1', 'lvl-2.1'), ('lvl-1', 'lvl-2.2'), ('lvl-2.1', 'lvl-3.1'), ('lvl-2.1', 2), ('lvl-2.2', 4), ('lvl-2.2', 6), ('lvl-3.1', 'lvl-4.1'), ('lvl-3.1', 5), ('lvl-4.1', 1), ('lvl-4.1', 3), ('input', 'lvl-1')]
            graph = nx.DiGraph()
            graph.add_edges_from(edges)
            nx.draw(graph, with_labels=True, node_size=1000, node_color="lightgray")
    ui.timer(1.0, some_graph)
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_custom_node_icons.html#sphx-glr-auto-examples-drawing-plot-custom-node-icons-py
    ui.run_with(app)

    