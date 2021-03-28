import xml.etree.ElementTree as ET
from typing import Dict, Set
from database import insert_document

file = 'Polytech_total.graphml'

vselennaya_file = 'vsel_own_full.graphml'
zhizn_file = 'Zhizn_own_full.graphml'
yazik_file = 'yazik_own_full.graphml'
nauka_file = 'nauka_own_full.graphml'
mozg_file = 'mozg_own_full.graphml'
medistina_file = 'meditsina_own_full.graphml'
materiya_file = 'materiya_own_full.graphml'
materialy_file = 'materialy_own_full.graphml'
IT_file = 'IT_own_full.graphml'
energiya_file = 'energiya_own_full.graphml'
dvizhenie_file = 'dvizhenie_own_full.graphml'


class Vertex:
    def __init__(self, id=None, color=None, label=None, topics=None):
        self.id = id
        self.label = label
        self.color = color
        self.topic = topics
        self.edges = []

    def __str__(self):
        return f'Vertex({self.id},{self.color},{self.label},{self.topic},{self.edges})'

    def toDict(self):
        return {
            'id': self.id,
            'color': self.color,
            'label': self.label,
            'topic': list(self.topic),
            'edges': [{'target_id': i, 'label': l} for i, l in self.edges]
        }


typing = '{http://graphml.graphdrawing.org/xmlns}'
yworks = '{http://www.yworks.com/xml/graphml}'

zhizn = set()
yazik = set()
vselennaya = set()
nauka = set()
mozg = set()
medistina = set()
materiya = set()
materialy = set()
IT = set()
energiya = set()
dvizhenie = set()


def update_topic_sets(file: str, topic: set):
    tree = ET.parse(file)
    root = tree.getroot()

    graph = root.find(typing + 'graph')

    child: ET.Element

    for child in graph:
        if child.tag == typing + 'node':
            for data in child:
                for shape in data:
                    shape: ET.Element
                    label = shape.find(yworks + 'NodeLabel').text
                    topic.add(label)


def get_topics(label) -> Set[str]:
    topics = {'all'}
    if label in zhizn:
        topics.add('zhizn')
    if label in yazik:
        topics.add('yazik')
    if label in vselennaya:
        topics.add('vselennaya')
    if label in nauka:
        topics.add('nauka')
    if label in mozg:
        topics.add('mozg')
    if label in medistina:
        topics.add('medistina')
    if label in materiya:
        topics.add('materiya')
    if label in materialy:
        topics.add('materialy')
    if label in IT:
        topics.add('IT')
    if label in energiya:
        topics.add('energiya')
    if label in dvizhenie:
        topics.add('dvizhenie')
    return topics


def parser_graphml(file) -> Dict[str, Vertex]:
    G: Dict[str, Vertex] = dict()

    tree = ET.parse(file)
    root = tree.getroot()

    graph = root.find(typing + 'graph')

    child: ET.Element

    for child in graph:
        if child.tag == typing + 'node':
            id = child.attrib['id']

            color = label = None

            for data in child:
                for shape in data:
                    shape: ET.Element
                    color = shape.find(yworks + 'Fill').attrib['color']
                    label = shape.find(yworks + 'NodeLabel').text
                    topics = get_topics(label)
            G[id] = Vertex(id, color, label, topics)

        if child.tag == typing + 'edge':
            v1 = child.attrib['source']
            v2 = child.attrib['target']
            label = None
            for data in child:
                for lineEngine in data:
                    lineEngine: ET.Element
                    if lineEngine.find(yworks + 'EdgeLabel') is not None:
                        label = lineEngine.find(yworks + 'EdgeLabel').text
            G[v1].edges.append((v2, label))
    return G


update_topic_sets(vselennaya_file, vselennaya)
update_topic_sets(dvizhenie_file, dvizhenie)
update_topic_sets(zhizn_file, zhizn)
update_topic_sets(nauka_file, nauka)
update_topic_sets(mozg_file, mozg)
update_topic_sets(medistina_file, medistina)
update_topic_sets(materiya_file, materiya)
update_topic_sets(materialy_file, materialy)
update_topic_sets(IT_file, IT)
update_topic_sets(energiya_file, energiya)
update_topic_sets(yazik_file, yazik)

G = parser_graphml(file)

#for vertex in G:
#    insert_document(G[vertex].toDict())
