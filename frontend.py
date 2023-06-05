from fastapi import FastAPI
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib import pyplot as plt
import datamodel
from nicegui import ui

## is to be the front-end part using nicegui
def init(app: FastAPI) -> None:
    @ui.page('/')
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
            G = nx.DiGraph()
            G.add_node("CENTRAL")
            nodes = ['CMC1','CMC2','HF1001','HF2001']
            # G.add_node("CMC1")
            # G.add_node("CMC2")
            # G.add_node("HF1001")
            # G.add_node("HF2001")
            for n in nodes:
                G.add_node(n)

            # G.add_node("su0112330")
            # G.add_node("su0112332")

            edges = [{"CENTRAL":"CMC1"},{"CENTRAL" : "CMC2"}]

            # G.add_edge("CENTRAL", "CMC1")
            # G.add_edge("CENTRAL", "CMC2")
            for e in edges:
                for i in e.items():
                    G.add_edge(i[0], i[1])
            G.add_edge("CMC2", "HF2001")
            G.add_edge("CMC2", "HF2002")
            G.add_edge("CMC1", "HF1001")
            G.add_edge("HF2001", "Anlaeg2001")
            G.add_edge("HF2001", "Anlaeg2002")
            G.add_edge("HF1001", "Anlaeg1001")


            ## TODO: adding customers
            # G.add_edge("Anlaeg2001","su0112330")
            # G.add_edge("Anlaeg1001","su0112332")


            # same layout using matplotlib with no labels
            plt.title('draw_networkx')
            pos=graphviz_layout(G, prog='dot')
            nx.draw(G, pos, with_labels=True, arrows=True)
    ui.timer(1.0, some_graph)
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_custom_node_icons.html#sphx-glr-auto-examples-drawing-plot-custom-node-icons-py
    ui.run_with(app)

    