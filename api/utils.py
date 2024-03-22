from datetime import datetime, date
from enum import Enum
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import re
import os
import requests
import json

load_dotenv()


class DBCrudOperation(Enum):
    FETCH = "fetch"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"

# The `DataCubeConnection` class provides methods for fetching, inserting, updating, and deleting data
# from a data cube using CRUD operations.


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
        "service_id": "DOWELL10039"
    }
    response = requests.post(url, json=payload)

    return json.loads(response.text)


def create_cs_db_meta(workspace_id):
    api_key = os.getenv("API_KEY")
    data_cube = DataCubeConnection()

    is_db = data_cube.fetch_data(api_key=api_key, db_name="customer_support_meta", coll_name="db_meta", filters={
                                 "name": f"{workspace_id}_customer_support"}, limit=1, offset=0)
    if not is_db['data']:
        response = data_cube.insert_data(api_key=api_key, db_name="customer_support_meta", coll_name="server", data={
                                         "name": f"{workspace_id}_customer_support"})
        return response
    else:
        return "DB already exists"


def check_db(workspace_id, db_name=None):
    api_key = os.getenv("API_KEY")
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
            create_cs_db_meta(workspace_id)
            return True
    else:
        return True


def check_collection(workspace_id, coll, db_name=None):
    api_key = os.getenv("API_KEY")
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

ORG_ID = "646ba835ce27ae02d024a902"
# if api_key is None:
#     raise ValueError("API_KEY is missing. Make sure it is set in the .env file.")
data_cube = DataCubeConnection()

# reponse = data_cube.delete_data(api_key=api_key,db_name="646ba835ce27ae02d024a902_CUSTOMER_SUPPORT_DB0", coll_name="topics", query={"name":"customer_support"})
# print(reponse)
# print(check_collection("646ba835ce27ae02d024a902", "server"))

# reponse = data_cube.update_data(api_key=api_key,db_name="646ba835ce27ae02d024a902_CUSTOMER_SUPPORT_DB0", coll_name="line_manager", query={"user_id":"Charu_Dowell"},update_data={"ticket_count": 14})
# print(reponse)


def set_finalize(linkid):
    url = f"https://www.qrcodereviews.uxlivinglab.online/api/v3/masterlink/?link_id={linkid}"
    payload = {
        "is_opened": True,
    }
    response = requests.put(url, json=payload)
    return response.text


def get_link_usernames(links):
    public_link_ids = []

    for link_info in links:
        link = link_info.get('link', '')
        parsed_url = urlparse(link)

        fragment_params = parse_qs(parsed_url.fragment)
        public_link_id = fragment_params.get('public_link_id', [None])[0]

        public_link_ids.append(public_link_id)

    return public_link_ids


def get_room_details(workspace_id, api_key, product, category_id):
    """
    The function `get_room_details` retrieves room details based on workspace ID, API key, product, and
    category ID.

    :param workspace_id: Workspace ID is a unique identifier for a specific workspace or environment
    where the data is stored or accessed. It helps in distinguishing different workspaces within a
    system
    :param api_key: An API key is a unique identifier used to authenticate a user, developer, or calling
    program to an API (Application Programming Interface). It is typically a long string of alphanumeric
    characters that grants access to specific resources or services
    :param product: Product is a variable that represents the type of product or service related to the
    room details being fetched
    :param category_id: Category ID is the identifier for a specific category within the workspace. It
    is used to filter and retrieve room details for that particular category
    :return: The function `get_room_details` returns the data fetched from the database based on the
    provided workspace_id, api_key, product, and category_id. If the collection "category" exists in the
    workspace, it fetches data using the `data_cube.fetch_data` function with specified filters and
    returns the data if the operation is successful. If the collection "category" does not exist, an
    empty list
    """
    db_name = f"{workspace_id}_{product}"
    coll_name = f"{workspace_id}_public_room"

    if check_collection(workspace_id, "category"):
        response = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={
                                        "category": category_id}, limit=20, offset=0)
        print(response)
        if response['success']:
            return response['data']
        else:
            return []
    else:
        return []


def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[^\w.]+', '_', filename)
    return sanitized_filename


def get_safe_timestamp():
    return datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')[:-3]


# workspace_id = "6385c0f18eca0fb652c94558"
# api_key = "1b834e07-c68b-4bf6-96dd-ab7cdc62f07f"
# product="customer_support"
# category_id = "65ba4d6ec5b56cc2cabc9221"

def check_daily_collection(workspace_id, product):
    """
    product=db_name
    """
    formatted_date = str(date.today()).replace("-", "_")

    api_key = os.getenv("API_KEY")
    data_cube = DataCubeConnection()

    db_name = f"{workspace_id}_{product}"
    coll_name = f"{workspace_id}_{formatted_date}_collection"

    collection_response = data_cube.fetch_data(
        api_key=api_key, db_name=db_name, coll_name=coll_name, filters={}, limit=1, offset=0)

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


def get_database_collections(api_key, db_name):
    """
    Retrieve a list of collections in the DataCube database.

    :param api_key: The API key for authentication.
    :param db_name: The name of the database.
    :return: A list containing only the collections with "_collection" in their names.
    """
    url = "https://datacube.uxlivinglab.online/db_api/collections/"
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


def fetch_data_from_collections(api_key, db_name, collections, filters, limit=50, offset=0):
    """
    This Python function fetches data from multiple collections using specified filters, limit, and
    offset parameters.

    :param api_key: The `api_key` parameter is typically a unique identifier or authentication token
    that grants access to the API services. 
    :param db_name: The `db_name` parameter in the `fetch_data_from_collections` function refers to the
    name of the database from which you want to fetch data.
    :param collections: Collections is a list of collection names from which data needs to be fetched
    :param filters: Filters are conditions or criteria used to retrieve specific data from a database or
    collection. 
    :param limit: The `limit` parameter in the `fetch_data_from_collections` function specifies the
    maximum number of records to retrieve from each collection.
    :param offset: The `offset` parameter in the `fetch_data_from_collections` function is used to
    specify the starting point from which data should be fetched. 
    :return: The function `fetch_data_from_collections` returns a list of data fetched from the
    specified collections based on the provided API key, database name, filters, limit, and offset
    parameters.
    """
    data = []
    for coll_name in collections:
        data_response = data_cube.fetch_data(
            api_key=api_key, db_name=db_name, coll_name=coll_name, filters=filters, limit=limit, offset=offset)
        if data_response['data']:
            data.extend(data_response['data'])
    return data


def assign_ticket_to_line_manager(api_key, db_name, coll_name, filters, limit=199, offset=0):
    """
    Assign a ticket to a line manager based on round-robin algorithm and specific conditions.

    :param api_key: The API key for authentication.
    :param db_name: The name of the database.
    :param coll_name: The name of the collection containing line manager data.
    :param filters: Filters to apply while retrieving line manager data.
    :param limit: Maximum number of line managers to retrieve (default is 199).
    :param offset: Offset for pagination (default is 0).
    :return: The user_id of the assigned line manager or None if no line manager available.
    """
    response = data_cube.fetch_data(
        api_key=api_key,
        db_name=db_name,
        coll_name=coll_name,
        filters=filters,
        limit=limit,
        offset=offset
    )

    line_managers = response['data']
    line_managers.sort(key=lambda x: (
        x['ticket_count'], x['positions_in_a_line']))

    for line_manager in line_managers:
        if line_manager['ticket_count'] == 0:
            line_manager['ticket_count'] += 1
            data_cube.update_data(
                api_key=api_key,
                db_name=db_name,
                coll_name=coll_name,
                query={'_id': line_manager['_id']},
                update_data={'ticket_count': line_manager['ticket_count']}
            )
            return line_manager['user_id']

    # If all line managers have ongoing tickets, assign to the one with the lowest ticket_count and positions_in_a_line
    if line_managers:
        line_manager = line_managers[0]
        line_manager['ticket_count'] += 1
        data_cube.update_data(
            api_key=api_key,
            db_name=db_name,
            coll_name=coll_name,
            query={'_id': line_manager['_id']},
            update_data={'ticket_count': line_manager['ticket_count']}
        )
        return line_manager['user_id']
    else:
        return None


def calculate_position_in_line(api_key, workspace_id):
    try:
        # Retrieve line managers
        line_manager_db_name = f"{workspace_id}_CUSTOMER_SUPPORT_DB0"
        line_manager_coll_name = "line_manager"
        line_managers_data = data_cube.fetch_data(
            api_key=api_key,
            db_name=line_manager_db_name,
            coll_name=line_manager_coll_name,
            filters={},
            limit=0,  # Fetch all line managers
            offset=0
        )

        # Extract positions_in_a_line from line managers data
        positions = [line_manager['positions_in_a_line']
                     for line_manager in line_managers_data['data']]

        # Sort positions to find gaps and the highest position
        positions.sort()
        highest_position = 0
        for pos in positions:
            if pos - highest_position > 1:
                return highest_position + 1
            highest_position = pos

        # If no gaps, return the next position after the highest
        return highest_position + 1
    except Exception as e:
        # Handle exceptions
        raise e


"""Dowell Mail API services"""


def send_email(toname, toemail, subject, email_content):
    url = "https://100085.pythonanywhere.com/api/email/"

    payload = {
        "toname": toname,
        "toemail": toemail,
        "subject": subject,
        "email_content": email_content
    }
    response = requests.post(url, json=payload)
    print(response.text)
    return response.text


EMAIL_FROM_WEBSITE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New Ticket Confirmation</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body style="font-family: Arial, sans-serif; background-color: #f7f7f7;">
    <div style="max-width: 600px; margin: 20px auto; padding: 0; text-align: center;">
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 15px 15px 0 0;">
            <img src="https://www.uxlivinglab.org/wp-content/uploads/2023/08/logo-e1531386713115.webp" alt="Company Logo" style="max-width: 150px; height: auto;">
        </div>
        <div style="background-color: #fff; border-radius: 0 0 15px 15px; padding: 30px; margin-bottom: 20px;">
            <h3 style="font-size: 24px; margin-bottom: 20px;">Your ticket {} has been opened</h3>
            <p style="font-size: 18px; margin-bottom: 20px; text-align: left;">Hello Customer,</p>
            <p style="font-size: 18px; margin-bottom: 20px; text-align: left;">Thank you for contacting us. Your ticket has been received and will be answered shortly. The details of your ticket are shown below:</p>
            <div style="text-align: left; margin-bottom: 20px;">
                <p><strong>Ticket ID:</strong> {}</p>
                <p><strong>Priority:</strong> Normal</p>
                <p><strong>Status:</strong> Open</p>
            </div>
            <a href="https://www.dowellchat.uxlivinglab.online" style="display: inline-block; background-color: #007bff; color: #fff; text-decoration: none; font-size: 16px; padding: 10px 20px; border-radius: 5px; border: none;">View Ticket</a>

        </div>
        <div style="font-size: 14px; margin-bottom: 20px;">
            <p>DoWell UX LivingLab</p>
        </div>
    </div>
</body>
</html>

"""


def is_valid_email(email):
    # Regular expression pattern for a basic email address validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Use re.match to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


# Example usage:

# db_name = "646ba835ce27ae02d024a902_CUSTOMER_SUPPORT_DB0"
# coll_name = "line_manager"
# filters = {}

# line_manager_id = assign_ticket_to_line_manager(api_key, db_name, coll_name, filters)
# if line_manager_id:
#     print("Ticket assigned to line manager:", line_manager_id)
# else:
#     print("No line manager available.")


# reponse = data_cube.update_data(api_key=api_key,db_name="646ba835ce27ae02d024a902_CUSTOMER_SUPPORT_DB0", coll_name="line_manager", query={"user_id":"646ba835ce27ae02d024a902"},update_data={"ticket_count":6})
# print(reponse)
