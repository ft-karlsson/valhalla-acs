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

    # @ui.page('/graph')
    # def some_graph():
    #     with ui.pyplot(figsize=(10, 5)):
                    
    #                 G = nx.Graph()
    #                 G.add_edge(1, 2)
    #                 G.add_edge(1, 3)
    #                 G.add_edge(1, datamodel.graphtest['test']['one'])
    #                 G.add_edge(2, 3)
    #                 G.add_edge(3, 4)

    #                 G.add_edge(4, 5)


    #                 # explicitly set positions
    #                 # pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}

    #                 options = {
    #                     "font_size": 36,
    #                     "node_size": 3000,
    #                     "node_color": "white",
    #                     "edgecolors": "black",
    #                     "linewidths": 5,
    #                     "width": 5,
    #                 }
    #                 nx.draw_networkx(G, **options)

    #                 # Set margins for the axes so that nodes aren't clipped
    #                 ax = plt.gca()
    #                 ax.margins(0.20)
    #                 plt.axis("off")
    # ui.timer(1.0, some_graph)
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_custom_node_icons.html#sphx-glr-auto-examples-drawing-plot-custom-node-icons-py
    ui.run_with(app)

