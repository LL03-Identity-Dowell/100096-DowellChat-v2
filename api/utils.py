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

    # def __init__(self, api_key):
    #     self.api_key = api_key

    def _make_request(self, operation, payload):
        url = self.GET_DATA_URL if operation == DBCrudOperation.FETCH else self.CRUD_URL
        if operation == DBCrudOperation.UPDATE:
            res = requests.put(url, json=payload)
        elif operation == DBCrudOperation.DELETE:
            res = requests.delete(url, json=payload)
        else:    
            res = requests.post(url, json=payload)
        return json.loads(res.text)

    def fetch_data(self, api_key, db_name, coll_name, filters, limit, offset):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.FETCH.value,
            "filters": filters,
            "limit": limit,
            "offset": offset,
        }
        return self._make_request(DBCrudOperation.FETCH, payload)

    def insert_data(self,api_key, db_name, coll_name, data):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.INSERT.value,
            "data": data,
        }
        return self._make_request(DBCrudOperation.INSERT, payload)

    def update_data(self, api_key, db_name, coll_name, query, update_data):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.UPDATE.value,
            "query": query,
            "update_data": update_data,
        }
        return self._make_request(DBCrudOperation.UPDATE, payload)

    def delete_data(self, api_key, db_name, coll_name, query):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.DELETE.value,
            "query": query,
        }
        return self._make_request(DBCrudOperation.DELETE, payload)


def processApiService(api_key):
    """The purpose of this request is to process the API key 
    and determine if it is valid for the specified API service."""
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'
    
    payload = {
        "service_id" : "DOWELL10039"
    }
    response = requests.post(url, json=payload)

    return json.loads(response.text)

def create_cs_db_meta(workspace_id):
    api_key = os.getenv("API_KEY")
    data_cube = DataCubeConnection()

    is_db =  data_cube.fetch_data(api_key=api_key,db_name="customer_support_meta", coll_name="db_meta", filters={"name": f"{workspace_id}_customer_support"}, limit=1, offset=0)
    if not is_db['data']:
        response = data_cube.insert_data(api_key=api_key,db_name="customer_support_meta", coll_name="server", data={"name":f"{workspace_id}_customer_support"})
        return response
    else:
        return "DB already exists"
    
def check_db(workspace_id):
    api_key = os.getenv("API_KEY")
    data_cube = DataCubeConnection()

    db_name = f"{workspace_id}_customer_support"
    coll_name = f"{workspace_id}_server"
    db_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0)
    if not db_response['success']:
        if "Database" in db_response['message']:
            return False
        else:
            create_cs_db_meta(workspace_id)
            return True
    else:
        return True
def check_collection(workspace_id, coll):
    api_key = os.getenv("API_KEY")
    data_cube = DataCubeConnection()

    db_name = f"{workspace_id}_customer_support"
    coll_name = f"{workspace_id}_{coll}"
    collection_response = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0)
    if not collection_response['success']:
        if "Collection" in collection_response['message']:
            url = "https://datacube.uxlivinglab.online/db_api/add_collection/"
            data_to_add = {
                "api_key": api_key,
                "db_name": db_name,
                "coll_names": coll_name,
                "num_collections": 1
            }
            response = requests.post(url, json=data_to_add)
            return True 
        else:
            return True   
    else:
        return True


"""DATACUBE USAGE"""
api_key = os.getenv("API_KEY")

# ORG_ID = "646ba835ce27ae02d024a902"
# if api_key is None:
#     raise ValueError("API_KEY is missing. Make sure it is set in the .env file.")
data_cube = DataCubeConnection()

# reponse = data_cube.fetch_data(api_key=api_key, db_name="dowellchat", coll_name="chat", filters={}, limit=1, offset=0)
# print(reponse)
# print(check_collection("646ba835ce27ae02d024a902", "server"))

# print(check_db("646ba835ce27ae02d024a902"))

def set_finalize(linkid):
    # print(linkid)
    url = f"https://www.qrcodereviews.uxlivinglab.online/api/v3/masterlink/?link_id={linkid}"
    payload = {
        "is_opened": True,
    }
    response = requests.put(url, json=payload)
    # print(response)
    # print(response.text)
    return response.text

# print(set_finalize("6155348369150513646"))