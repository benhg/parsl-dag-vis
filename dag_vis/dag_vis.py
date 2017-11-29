from parsl.dataflow.states import States
from IPython.core.display import Javascript, HTML, Javascript, display
import json


class DFKListener():
    def __init__(self, dfk):
        self.dfk = dfk
        self.nodes_list = []
        self.edges_list = []
        self.color_lookup_table = {
            States.unsched: "Pink",
            States.pending: "Yellow",
            States.runnable: "Blue",
            States.running: "Lime",
            States.done: "Green",
            States.failed: "Red",
            States.dep_fail: "orange"
        }
        self.state_lookup_table = {
            States.unsched: "Unscheduled",
            States.pending: "Pending",
            States.runnable: "Runnable",
            States.running: "Running",
            States.done: "Finished",
            States.failed: "Failed",
            States.dep_fail: "Dependency Failure"
        }

    @property
    def nodes(self):
        return self.nodes_list

    @property
    def edges(self):
        return self.edges_list

    def create_nodes(self, dfke=None):
        dfk = dfke if dfke else self.dfk
        for task in dfk.tasks:
            state = dfk.tasks[task]['status']
            tid = dfk.tasks[task]['app_fu'].tid
            task = {"id": tid, "label": tid, "color": self.color_lookup_table[state], "font": {
                "background": "white"}, "title": self.state_lookup_table[state]}
            self.nodes_list.append(task)
            self.nodes_list = list(
                {v['id']: v for v in self.nodes_list}.values())
        return self.nodes_list

    def create_edges(self, dfke=None):
        dfk = dfke if dfke else self.dfk
        for task in dfk.tasks:
            deps = state = dfk.tasks[task]['depends']
            for dep in deps:
                edge = {"from": dep.tid, "to": task, "arrows": 'to'}
                self.edges_list.append(edge)
        return self.edges

    def update(self):
        self.create_nodes()
        self.create_edges()
        return json.dumps({"nodes": self.nodes, "edges": self.edges})

    def set_javascript(self):
        self.update()
        nodes = json.dumps(self.nodes)
        edges = json.dumps(self.edges)
        display(Javascript("""window.nodesList={};
                      window.edgesList={};
                   """.format(nodes, edges)))

    def show_window(self):
        display(Javascript("""require.config({paths: {vis: 'https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min'}});
require(['vis'], function (vis){
    element.append('<div id="mynetwork" style="width:950px;height:750px;border:1px solid lightgray;"></div>');
    var nodes = new vis.DataSet(window.nodesList);
    var edges = new vis.DataSet(window.edgesList);
    var container = document.getElementById('mynetwork');
    var data = {
         nodes: nodes,
         edges: edges
     };
     var options = {interaction:{hover:true}, 
                   layout: {
                    hierarchical: {
                        direction: 'UD'
                    }}
                   };
     var network = new vis.Network(container, data, options);
     network.on("hoverNode", function (params) {
             
     });
     network.on("hoverEdge", function (params) {
            
     });
     network.on("blurNode", function (params) {
             
     });
     network.on("blurEdge", function (params) {
             
     });
});"""))