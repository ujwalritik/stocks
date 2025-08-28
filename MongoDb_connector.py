from pymongo import MongoClient
def conn():
    connection_string = "mongodb://localhost:27017"
    client = MongoClient(connection_string)
    db = client["News"]
    collection = db["news_data"]
    return collection
