from abc import ABC, abstractmethod
import certifi
from pymongo import MongoClient


class save_to_db(ABC):
    @abstractmethod
    def save(self):
        pass


class mongodb(save_to_db):
    def __init__(self, databaseName = "PractiseDb"):
        CONNECTION_STRING = "mongodb+srv://subhankar:subhankar2028@cluster0.vwov3tz.mongodb.net/"+databaseName
        client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
        self.db = client[databaseName]

    def get_collection(self, collection_name):
        collection = self.db[collection_name]
        return collection

    def save(self, collection, data):
        collection_name = self.db[collection]
        collection_name.insert_one(data)
        return True


