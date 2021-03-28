import pymongo

# Create the client

host = 'mongodb://root:jsdavnsdancasdkhlvb2314jknsvb@87.249.221.208:5151/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
client = pymongo.MongoClient(host)

# Connect to our database
db = client['test']

# Fetch our series collection
series_collection = db['Vertexes']

def insert_document(data, collection=series_collection):
    """ Function to insert a document into a collection and
    return the document's id.
    """
    return collection.insert_one(data).inserted_id