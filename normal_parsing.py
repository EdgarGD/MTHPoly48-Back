import xml.etree.ElementTree as ET
from typing import Dict
from database import insert_document

file = 'Polytech_total.graphml'


class Vertex:
    def __init__(self, id=None, color=None, label=None):
        self.id = id
        self.label = label
        self.color = color
        self.topic = 'BasicTopic'
        self.edges = []

    def __str__(self):
        return f'Vertex({self.id},{self.color},{self.label},{self.topic},{self.edges})'

    def toDict(self):
        return {
            'id': self.id,
            'color': self.color,
            'label': self.label,
            'topic': self.topic,
            'edges': [{'target_id': i, 'label': l} for i, l in self.edges]
                }


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

for vertex in G.values():
    vertex: Vertex
    insert_document(vertex.toDict())