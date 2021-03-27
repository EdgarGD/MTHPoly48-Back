import xml.etree.ElementTree as ET
import networkx as nx
from typing import Dict

file = 'Polytech_total.graphml'#'vsel_own_full.graphml'


class Vertex:
    def __init__(self, id=None, color=None, label=None):
        self.id = id
        self.label = label
        self.color = color
        self.edges = []

    def __str__(self):
        return f'Vertex({self.id},{self.color},{self.label},{self.edges})'


G: Dict[str, Vertex] = dict()

tree = ET.parse(file)
root = tree.getroot()

typing = '{http://graphml.graphdrawing.org/xmlns}'
yworks = '{http://www.yworks.com/xml/graphml}'

graph = root.find(typing + 'graph')

child: ET.Element

for child in graph:
    if child.tag == typing + 'node':
        id = child.attrib['id']

        color = label = None

        for data in child:
            for shape in data:
                shape: ET.Element
                color = shape.find(yworks+'Fill').attrib['color']
                label = shape.find(yworks+'NodeLabel').text
        G[id] = Vertex(id, color, label)

    if child.tag == typing + 'edge':
        v1 = child.attrib['source']
        v2 = child.attrib['target']
        label = None
        for data in child:
            for lineEngine in data:
                lineEngine: ET.Element
                if lineEngine.find(yworks+'EdgeLabel') is not None:
                    label = lineEngine.find(yworks+'EdgeLabel').text
        G[v1].edges.append((v2, label))
