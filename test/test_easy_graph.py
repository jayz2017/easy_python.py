import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from easy_pyechart import easy_graph,set_water_marking,save_static_image,baseParams

def test_graph():
    _nodes = [{"name": "结点1", "symbolSize": 10},
         {"name": "结点2", "symbolSize": 20},
         {"name": "结点3", "symbolSize": 30},
         {"name": "结点4", "symbolSize": 40},
         {"name": "结点5", "symbolSize": 50},
         {"name": "结点6", "symbolSize": 40},
         {"name": "结点7", "symbolSize": 30},
         {"name": "结点8", "symbolSize": 20}]
    _links=[]
    for i in _nodes:
        for j in _nodes:
            _links.append({"source": i.get('name'), "target": j.get('name')})

    easy_graph.eGraph(nodes=_nodes).excute_eGraph(baseParams(title='测试',subTitle="")).render("graph_base.html")
#test_graph()