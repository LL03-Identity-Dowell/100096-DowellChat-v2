import os
import requests
import json
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

class DBCrudOperation(Enum):
    FETCH = "fetch"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"

class DataCubeConnection:
    BASE_URL = "https://datacube.uxlivinglab.online/db_api/"
    CRUD_URL = BASE_URL + "crud/"
    GET_DATA_URL = BASE_URL + "get_data/"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, operation, payload):
        url = self.GET_DATA_URL if operation == DBCrudOperation.FETCH else self.CRUD_URL
        if operation == DBCrudOperation.UPDATE:
            res = requests.put(url, json=payload)
        else:    
            res = requests.post(url, json=payload)
        return json.loads(res.text)

    def fetch_data(self, db_name, coll_name, filters, limit, offset):
        payload = {
            "api_key": self.api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.FETCH.value,
            "filters": filters,
            "limit": limit,
            "offset": offset,
        }
        return self._make_request(DBCrudOperation.FETCH, payload)

    def insert_data(self, db_name, coll_name, data):
        payload = {
            "api_key": self.api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.INSERT.value,
            "data": data,
        }
        return self._make_request(DBCrudOperation.INSERT, payload)

    def update_data(self, db_name, coll_name, query, update_data):
        payload = {
            "api_key": self.api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.UPDATE.value,
            "query": query,
            "update_data": update_data,
        }
        return self._make_request(DBCrudOperation.UPDATE, payload)

    def delete_data(self, db_name, coll_name, query):
        payload = {
            "api_key": self.api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.DELETE.value,
            "query": query,
        }
        return self._make_request(DBCrudOperation.DELETE, payload)


"""DATACUBE USAGE"""
api_key = os.getenv("API_KEY")

# if api_key is None:
#     raise ValueError("API_KEY is missing. Make sure it is set in the .env file.")
# data_cube = DataCubeConnection(api_key)
# updated_data = {
#                 "name": "test_updat",
#                 "member_list": 'member_list',
#                 "channels": 'channel',
#                 "events": 'events',
#                 "owner": 'owner',
#                 "created_at": 'created_at', 
#         }

# response = data_cube.update_data(db_name="dowellchat", coll_name="server", query = {"name": 'test_update'}, update_data=updated_data)    
# # response = data_cube.fetch_data(db_name="dowellchat", coll_name="serve", filters={"name": "test7"}, limit=1, offset=0)
# print(response)


# url = "https://datacube.uxlivinglab.online/db_api/crud/"

# data = {
#     "api_key": api_key,
#     "db_name": "dowellchat",
#     "coll_name": "server",
#     "operation": "update",
#     "query" : {"name": "test8"},
#     "update_data":updated_data
# }

# response = requests.put(url, json=data)
# print(response)

def processApiService(api_key):
    """The purpose of this request is to process the API key 
    and determine if it is valid for the specified API service."""
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    
    payload = {
        "service_id" : "DOWELL10039"
    }
    response = requests.post(url, json=payload)

    return json.loads(response.text)