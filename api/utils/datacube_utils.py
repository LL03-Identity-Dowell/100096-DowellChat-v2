import requests
from api.connector.database_connector import DataCubeConnection
from datetime import date
import json 

data_cube = DataCubeConnection()

def map_product_to_db(workspace_id, api_key, product):
    """
    Map a product to its corresponding database name.

    Args:
        workspace_id (str): The workspace ID.
        api_key (str): The API key for accessing data.
        product (str): The name of the product.

    Returns:
        str: The database name corresponding to the product, or "Product not found" if the product is not found.
    """
    try:
        check_topic = data_cube.fetch_data(
            api_key=api_key,
            db_name=f"{workspace_id}_cs_ticketing_system_db0",
            coll_name=f"{workspace_id}_topics",
            filters={"name": product.lower()},
            limit=1,
            offset=0
        )

        if check_topic.get('success', True) and check_topic.get('data'):
            response = check_topic.get('data')
            return response[0]["db_name"]
        else:
            return "Product not found"
    except Exception as e:
        return f"Error: {str(e)}"


def get_database_collections(api_key, db_name):
    """
    Retrieve a list of collections in the DataCube database.

    :param api_key: The API key for authentication.
    :param db_name: The name of the database.
    :return: A list containing only the collections with "_collection" in their names.
    """
    # url = "https://datacube.uxlivinglab.online/db_api/collections/"
    url = "https://www.dowelldatacube.uxlivinglab.online/db_api/collections/"
    payload = {
        "api_key": api_key,
        "db_name": db_name,
        "payment": False
    }
    response = requests.get(url, json=payload)
    if response.json()['data']:
        data = response.json()['data'][0]
        filtered_collections = [
            collection for collection in data if '_collection' in collection]
        return filtered_collections
    else:
        return []
    
def check_connection():
    """
        Checks connection to socket
    """
    try:
        response = requests.get('https://1000093.pythonanywhere.com/connect/')
        res = json.loads(response.text)
        if response.status_code == 200:
            if res['status'] == True:
                return True
            else:
                return False
        else:
            return False
    except:
        return False    
def check_daily_collection(api_key, workspace_id, product):
    """
    product=db_name
    """
    formatted_date = str(date.today()).replace("-", "_")

    data_cube = DataCubeConnection()

    db_name = map_product_to_db(workspace_id, api_key, product)
    coll_name = f"{workspace_id}_{formatted_date}_{product}_collection"

    collection_response = data_cube.fetch_data(
        api_key=api_key, db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0)

    if not collection_response['success']:
        if "Collection" in collection_response['message']:
            # url = "https://datacube.uxlivinglab.online/db_api/add_collection/"
            url = "https://www.dowelldatacube.uxlivinglab.online/db_api/add_collection/"
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

def check_collection(api_key, workspace_id, coll, db_name=None):
    data_cube = DataCubeConnection()

    if db_name:
        db_name = db_name
        coll_name = coll
    else:
        db_name = f"{workspace_id}_customer_support"
        coll_name = f"{workspace_id}_{coll}"

    collection_response = data_cube.fetch_data(
        api_key=api_key, db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0)
    if not collection_response['success']:
        if "Collection" in collection_response['message']:
            # url = "https://datacube.uxlivinglab.online/db_api/add_collection/"
            url = "https://www.dowelldatacube.uxlivinglab.online/db_api/add_collection/"
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


def create_cs_db_meta(api_key, workspace_id):
    data_cube = DataCubeConnection()

    is_db = data_cube.fetch_data(api_key=api_key, db_name="customer_support_meta", coll_name="db_meta", filters={
                                 "name": f"{workspace_id}_customer_support"}, limit=1, offset=0)
    if not is_db['data']:
        response = data_cube.insert_data(api_key=api_key, db_name="customer_support_meta", coll_name="server", data={
                                         "name": f"{workspace_id}_customer_support"})
        return response
    else:
        return "DB already exists"


def check_db(workspace_id, api_key, db_name=None):
    data_cube = DataCubeConnection()

    if db_name:
        db_name = db_name
        coll_name = f"{workspace_id}_server"
    else:
        db_name = f"{workspace_id}_customer_support"
        coll_name = f"{workspace_id}_server"
    db_response = data_cube.fetch_data(
        api_key=api_key, db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0) 
    if not db_response['success']:
        if "Database" in db_response['message']:
            return False
        else:
            return True
    else:
        return True
    
