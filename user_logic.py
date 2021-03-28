from typing import List, Dict

import pymongo

host = 'mongodb://root:jsdavnsdancasdkhlvb2314jknsvb@87.249.221.208:5151/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
client = pymongo.MongoClient(host)
TOPICS = [
    "zhizn",
    "yazik",
    "vselennaya",
    "nauka",
    "mozg",
    "medistina",
    "materiya",
    "maretialy",
    "IT",
    "energiya",
    "dvizhenie"
]

# Connect to our database
db = client['test']

# Fetch our series collection
series_collection = db['Users']

users = []

def document_user(user_id = None, answers = None, interests = None, name: str = None, age: int = None):
    data = {'name':name, 'age': age}
    document = {'user_id': user_id,'user_data': data, 'user_answers': answers, 'user_interests': interests}


    if user_id in users:
        data['name'] = name or series_collection.find_one({'user_id':user_id})['user_data']['name']
        data['age'] = age or series_collection.find_one({'user_id':user_id})['user_data']['age']

        document['user_answers'] = answers or document['user_answers']
        document['user_interests'] = interests or document['user_interests']

    return document

def get_users():
    i = len(users)+1
    while series_collection.count_documents({'user_id': f'u{i}'}) > 0:
        users.append(f'u{i}')
        i += 1

def add_user(name: str = 'Ivan', age: int = 16):
    series_collection.insert_one(document_user(user_id=f'u{len(users)+1}',name=name, age=age))
    get_users()


def faq_results(answers: List[bool] = None, user_id: str = None,) -> Dict[str, bool]:
    if answers is None:
        answers = [False,] * len(TOPICS)
    elif len(answers) < len(TOPICS):
        answers = answers + [False] * (len(TOPICS)-len(answers))
    if user_id is None:
        user_id = users[-1]
    interests: Dict[str, bool] = {TOPICS[i] : answers[i] for i in range(len(TOPICS))}


    document = document_user(user_id=user_id, answers=answers, interests=interests)
    series_collection.find_one_and_replace({'user_id': user_id}, document)
    return document


get_users()