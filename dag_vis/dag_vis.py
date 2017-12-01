from parsl.dataflow.states import States
from IPython.core.display import Javascript, HTML, Javascript, display
import json
from threading import Thread


class DFKListener():
    def __init__(self, dfk):
        """Set necessary global options and variables"""
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
            States.dep_fail: "Orange"
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
        """define list of nodes as an instance variable"""
        return self.nodes_list

    @property
    def edges(self):
        """Define list of edges as an instance variable"""
        return self.edges_list

    def create_nodes(self, dfke=None):
        """Go through dfk's task listing and 
        create a node in our graph for each task"""
        dfk = dfke if dfke else self.dfk
        for task in dfk.tasks:
            state = dfk.tasks[task]['status']
            if state == States.done:
                if dfk.tasks[task]["exec_fu"]._exception is not None:
                    state = States.failed
            tid = dfk.tasks[task]['app_fu'].tid
            fname = dfk.tasks[task]['func'].__name__
            task = {"id": tid, "label": "{}\n{}\n{}".format(str(tid), fname, self.state_lookup_table[state]), "color": self.color_lookup_table[state], "font": {
                "background": "white"}, "title": self.state_lookup_table[state]}
            self.nodes_list.append(task)
            self.nodes_list = list(
                {v['id']: v for v in self.nodes_list}.values())
        return self.nodes_list

    def create_edges(self, dfke=None):
        """Generate edges of dependency graph from list of tasks"""
        dfk = dfke if dfke else self.dfk
        for task in dfk.tasks:
            deps = state = dfk.tasks[task]['depends']
            for dep in deps:
                edge = {"from": dep.tid, "to": task, "arrows": 'to'}
                self.edges_list.append(edge)
        return self.edges

    def update(self):
        """Update lists of nodes and edges"""
        self.nodes_list = []
        self.edges_list = []
        self.create_nodes()
        self.create_edges()
        return json.dumps({"nodes": self.nodes, "edges": self.edges})

    def set_javascript(self):
        """Update lists and send data to javascript so it can be rendered
        as an interactive graph"""
        self.update()
        nodes = json.dumps(self.nodes)
        edges = json.dumps(self.edges)
        display(Javascript("""window.nodesList={};
                              window.edgesList={};
                   """.format(nodes, edges)))

    def show_window(self):
        """Create interactive graph object and populate it with live data"""
        display(Javascript("""require.config({paths: {vis: 'https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min'}});
require(['vis'], function (vis){
    if (document.getElementById("mynetwork") == null) {
        element.append('<div id="mynetwork" style="width:950px;height:750px;border:1px solid lightgray;"></div>');
    }
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

    def update_thread_handler(self, secs):
        """Handler to autoupdate the rendering of the dag"""
        import time
        while True:
            self.set_javascript()
            self.show_window()
            time.sleep(secs)

    def auto_updater(self, time):
        """Opens a thread to autoupdate the graph"""
        threads = []
        t = Thread(target=self.update_thread_handler, args=(time,))
        threads.append(t)
        t.start()
