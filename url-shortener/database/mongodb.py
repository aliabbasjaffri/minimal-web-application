import os
from pymongo import MongoClient


class MongoAPI:
    """
    Module to interact with MongoDb
    MongoDb instance is currently running in a docker
    container
    """

    def __init__(self, db_connection: str = "mongodb"):
        """
        This initializer creates the mongodb instance and
        configures it
        :param db_connection: the connection point of DB
        It can be either localhost or mongodb
        """
        mongo_username = os.getenv("MONGODB_USER", "root")
        mongo_password = os.getenv("MONGODB_PASS", "rootpassword")
        mongo_database = os.getenv("MONGO_DB_NAME", "url-shorten-db")

        self.client = MongoClient(
            "mongodb://{}:27017/".format(db_connection),
            username="{}".format(mongo_username),
            password="{}".format(mongo_password),
        )

        database = "{}".format(mongo_database)
        collection = "{}-collection".format(mongo_database)
        cursor = self.client[database]
        self.collection = cursor[collection]

    def insert(self, data: dict):
        """
        Inserts data in mongodb
        The data is already checked for validations and
        sanitations and is only persisted here.
        :param data: dict containing original and shortened urls
        :return: the data instance that it just inserted
        """
        try:
            self.collection.insert_one(data)
            return data
        except Exception as e:
            print("Exception ::", e)
            return None

    def read(self, data: dict):
        """
        Reads from the database based on the param provided
        :param data: a dictionary containing either url or
        shortened_url with its value
        :return: the URL object if found, otherwise an error message
        """
        try:
            _url = self.collection.find_one(data)
            if _url:
                return _url
            else:
                return {"message": "URL does not exist"}
        except Exception as e:
            print("Exception ::", e)
            return None

    def find(self, data: dict):
        """
        Finds an item in the database
        :param data: a dictionary containing either url or
        shortened_url with its value
        :return: either True or False based on whether the db
        has the value
        """
        try:
            _url = self.collection.find_one(data)
            if _url is not None:
                return True
            else:
                return False
        except Exception as e:
            print("Exception ::", e)
            return None

    def delete(self, data: dict):
        """
        Deletes from the database
        :param data: a dictionary containing either url or
        shortened_url with its value
        :return: A success or failure message
        """
        try:
            url_obj = self.collection.find_one(data)
            if url_obj:
                self.collection.delete_one(url_obj)
                return {"message": "Item deleted successfully", "statuscode": 204}
            else:
                return {"message": "User ID does not exist.", "statuscode": 404}
        except Exception as e:
            print("Exception ::", e)
            return None


if __name__ == "__main__":
    mongo = MongoAPI(db_connection="localhost")
    print(mongo.insert({"url": "https://www.google.com/"}))
    print(mongo.read({"url": "https://www.google.com/"}))
    print(mongo.find({"url": "https://www.goPogle.com/"}))
    print(mongo.find({"url": "https://www.google.com/"}))
    print(mongo.delete({"url": "https://www.google.com/"}))
