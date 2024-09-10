from enum import Enum
import requests
import json


class DBCrudOperation(Enum):
    FETCH = "fetch"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"

# The `DataCubeConnection` class provides methods for fetching, inserting, updating, and deleting data
# from a data cube using CRUD operations.


class DataCubeConnection:
    # BASE_URL = "https://datacube.uxlivinglab.online/db_api/"
    BASE_URL = "https://www.dowelldatacube.uxlivinglab.online/db_api/"
    CRUD_URL = BASE_URL + "crud/"
    GET_DATA_URL = BASE_URL + "get_data/"

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
            "payment": False
        }
        return self._make_request(DBCrudOperation.FETCH, payload)

    def insert_data(self, api_key, db_name, coll_name, data):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.INSERT.value,
            "data": data,
            "payment": False
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
            "payment": False
        }
        return self._make_request(DBCrudOperation.UPDATE, payload)

    def delete_data(self, api_key, db_name, coll_name, query):
        payload = {
            "api_key": api_key,
            "db_name": db_name,
            "coll_name": coll_name,
            "operation": DBCrudOperation.DELETE.value,
            "query": query,
            "payment": False
        }
        return self._make_request(DBCrudOperation.DELETE, payload)
