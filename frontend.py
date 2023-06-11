from fastapi import FastAPI
import datamodel
from nicegui import ui



def query(some_key):
    print(f"device is: {some_key}")
    if len(some_key) > 8:
        try:
            some_sub_data = datamodel.subscribers[some_key]
            device_serial = some_sub_data['devices'][0]['serialnumber']
            return "Device: " + device_serial
        
        except KeyError:
            return "Nothing found"            
    else:
        return "Need more characters.."

def wrapper_for_get(device_iq, param):
    if device_iq == '':
        # default to known serial for now
        print(device_iq)
        print(type(device_iq))
        device_iq = "SE1936018000231"
        try:
            man = datamodel.devices[device_iq]['manufacturer']
            return man
        except KeyError:
            return "Not found"

## is to be the front-end part using nicegui
def init(app: FastAPI) -> None:
    @ui.page('/')
    def show():
        device_in_question = ui.label()
        device_in_question.set_visibility(False)
        with ui.tabs() as tabs:
            ui.tab('Search', icon='home').classes('w-80')
            ui.tab('About', icon='info').classes('w-80')
            ui.tab('Devices', icon='router').classes('w-80')
            ui.tab('Subscribers', icon='people').classes('w-80')
            ui.tab('Policies', icon='poll')

        with ui.tab_panels(tabs, value='Search'):
            with ui.tab_panel('Search'):
                ui.label('Search for a subscriber').classes('w-40')
                ui.input(label='Subscriber', placeholder='start typing',
                on_change=lambda e: [result.set_text(query(e.value)), device_in_question.set_text(result.text)],
                validation={'Input too long': lambda value: len(value) < 20}).on('keydown.enter', lambda e: ui.tab_panels(tabs, value='Devices'))
                result = ui.label()

            with ui.tab_panel('About'):
                ui.label('This is the second tab')
            with ui.tab_panel('Devices'):
                ui.label('This is the devices tab')
                ui.label('write some more')
                with ui.grid(columns=2):
                    ui.label('device:')
                    device = ui.label()
                    # TODO: take argument instead
                    ui.timer(1.0, lambda: device.set_text(datamodel.devices['SE1936018000231']["manufacturer"]))
                    ui.label('serial:')
                    serial = ui.label()
                    ui.timer(1.0, lambda: serial.set_text(datamodel.devices['SE1936018000231']['serialnumber']))
            with ui.tab_panel('Subscribers').classes('w-150'):
                ui.label('This is the subscriber tab')
                grid = ui.aggrid({
                    'columnDefs': [
                        {'headerName': 'Name', 'field': 'first_name'},
                        {'headerName': 'subscriber_id', 'field': 'subscriber_id'},
                    ],
                    'rowData': list(datamodel.subscribers.values()),
                    'rowSelection': 'multiple',
                }).classes('w-80')
            with ui.tab_panel('Policies'):
                ui.label('This is the policies tab')
            with ui.tab_panel('Search'):
                ui.label('This is the search tab')


                    
    # @ui.page('/graph')
    # def some_graph():
    #     with ui.pyplot(figsize=(10, 5)):
    #         G = nx.DiGraph()
    #         G.add_node("CENTRAL")
    #         nodes = ['CMC1','CMC2','HF1001','HF2001']
    #         # G.add_node("CMC1")
    #         # G.add_node("CMC2")
    #         # G.add_node("HF1001")
    #         # G.add_node("HF2001")
    #         for n in nodes:
    #             G.add_node(n)

    #         # G.add_node("su0112330")
    #         # G.add_node("su0112332")

    #         edges = [{"CENTRAL":"CMC1"},{"CENTRAL" : "CMC2"}]

    #         # G.add_edge("CENTRAL", "CMC1")
    #         # G.add_edge("CENTRAL", "CMC2")
    #         for e in edges:
    #             for i in e.items():
    #                 G.add_edge(i[0], i[1])
    #         G.add_edge("CMC2", "HF2001")
    #         G.add_edge("CMC2", "HF2002")
    #         G.add_edge("CMC1", "HF1001")
    #         G.add_edge("HF2001", "Anlaeg2001")
    #         G.add_edge("HF2001", "Anlaeg2002")
    #         G.add_edge("HF1001", "Anlaeg1001")


    #         ## TODO: adding customers
    #         # G.add_edge("Anlaeg2001","su0112330")
    #         # G.add_edge("Anlaeg1001","su0112332")


    #         # same layout using matplotlib with no labels
    #         plt.title('draw_networkx')
    #         pos=graphviz_layout(G, prog='dot')
    #         nx.draw(G, pos, with_labels=True, arrows=True)
    # ui.timer(1.0, some_graph)
    # https://networkx.org/documentation/stable/auto_examples/drawing/plot_custom_node_icons.html#sphx-glr-auto-examples-drawing-plot-custom-node-icons-py
    ui.run_with(app)

    