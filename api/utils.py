from datetime import datetime, date
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import re
import os
import requests
import json
from api.connector.database_connector import DataCubeConnection

load_dotenv()




def processApiService(api_key):
    """The purpose of this request is to process the API key 
    and determine if it is valid for the specified API service."""
    url = f'https://100105.pythonanywhere.com/api/v3/process-services/?type=api_service&api_key={api_key}'

    payload = {
        "service_id": "DOWELL10039"
    }
    response = requests.post(url, json=payload)

    return json.loads(response.text)


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



data_cube = DataCubeConnection()


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
    where the data is stored or accessed. 
    :param api_key: An API key is a unique identifier used to authenticate a user, developer, or calling
    program to an API (Application Programming Interface). 
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


# def assign_ticket_to_line_manager(api_key, db_name, coll_name, filters, limit=199, offset=0):
#     """
#     Assign a ticket to a line manager based on round-robin algorithm and specific conditions.

#     :param api_key: The API key for authentication.
#     :param db_name: The name of the database.
#     :param coll_name: The name of the collection containing line manager data.
#     :param filters: Filters to apply while retrieving line manager data.
#     :param limit: Maximum number of line managers to retrieve (default is 199).
#     :param offset: Offset for pagination (default is 0).
#     :return: The user_id of the assigned line manager or None if no line manager available.
#     """
#     response = data_cube.fetch_data(
#         api_key=api_key,
#         db_name=db_name,
#         coll_name=coll_name,
#         filters=filters,
#         limit=limit,
#         offset=offset
#     )

#     line_managers = response['data']
#     line_managers.sort(key=lambda x: (
#         x['ticket_count'], x['positions_in_a_line']))

#     for line_manager in line_managers:
#         if line_manager['ticket_count'] == 0:
#             line_manager['ticket_count'] += 1
#             data_cube.update_data(
#                 api_key=api_key,
#                 db_name=db_name,
#                 coll_name=coll_name,
#                 query={'_id': line_manager['_id']},
#                 update_data={'ticket_count': line_manager['ticket_count']}
#             )
#             return line_manager['user_id']

#     # If all line managers have ongoing tickets, assign to the one with the lowest ticket_count and positions_in_a_line
#     if line_managers:
#         line_manager = line_managers[0]
#         line_manager['ticket_count'] += 1
#         data_cube.update_data(
#             api_key=api_key,
#             db_name=db_name,
#             coll_name=coll_name,
#             query={'_id': line_manager['_id']},
#             update_data={'ticket_count': line_manager['ticket_count']}
#         )
#         return line_manager['user_id']
#     else:
#         return None


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
    
    if not line_managers:
        return None
    
    line_managers.sort(key=lambda x: (x['ticket_count'], x['positions_in_a_line']))
    
    min_ticket_count = line_managers[0]['ticket_count']
    candidates = [lm for lm in line_managers if lm['ticket_count'] == min_ticket_count]
    
    candidates.sort(key=lambda x: x['positions_in_a_line'])
    
    assigned_line_manager = candidates[0]

    return assigned_line_manager['user_id']


def calculate_position_in_line(api_key, workspace_id):
    try:
        # Retrieve line managers
        line_manager_db_name = f"{workspace_id}_cs_ticketing_system_db0"
        line_manager_coll_name = f"{workspace_id}_line_manager"
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


def assign_database_to_product(workspace_id, api_key):
    check_topic = data_cube.fetch_data(
        api_key=api_key, 
        db_name=f"{workspace_id}_cs_ticketing_system_db0", 
        coll_name=f"{workspace_id}_topics", 
        filters={},
        limit=200, 
        offset=0)
    
    
    if check_topic.get('success', False) and not check_topic.get('data'):
        return f"{workspace_id}_db_topic_1"
    
    else:
        count = len(check_topic.get('data', []))
        print(count)
        next_db_index = count + 1
        return f"{workspace_id}_db_topic_{next_db_index}"

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


def get_unread_messages_for_line_manager(api_key, db_name, line_manager, coll_name):
    ticket_filters = {"document_type": "ticket", "line_manager": line_manager, "is_closed":False}
    tickets_response = data_cube.fetch_data(api_key=api_key, 
                                            db_name=db_name, 
                                            coll_name=coll_name,
                                            filters=ticket_filters,
                                            limit=100,
                                            offset=0)
    
    tickets = tickets_response.get('data', [])
    
    unread_messages = []
    unread_count = 0

    if tickets:
        for ticket in tickets:
            ticket_id = ticket["_id"]
            message_filters = {"document_type": "chat", "ticket_id": ticket_id, "is_read": False}
            messages_response = data_cube.fetch_data(api_key=api_key, 
                                                    db_name=db_name, 
                                                    coll_name=coll_name,
                                                    filters=message_filters,
                                                    limit=100,
                                                    offset=0)
            
            messages = messages_response.get('data', [])
            unread_messages.extend(messages)
            unread_count += len(messages)

    return unread_messages, unread_count


def update_line_manager_ticket_count(api_key, workspace_id, line_manager):
    try:
        # Fetch line manager data
        line_manager_data = data_cube.fetch_data(
            api_key=api_key,
            db_name=f"{workspace_id}_cs_ticketing_system_db0",
            coll_name=f"{workspace_id}_line_manager",
            filters={"user_id": line_manager},
            limit=1,
            offset=0
        )
        
        if line_manager_data['success'] and line_manager_data['data']:
            line_manager = line_manager_data['data'][0]
            line_manager['ticket_count'] += 1

            response = data_cube.update_data(
                api_key=api_key,
                db_name=f"{workspace_id}_cs_ticketing_system_db0",
                coll_name=f"{workspace_id}_line_manager",
                query={'_id': line_manager['_id']},
                update_data={'ticket_count': line_manager['ticket_count']}
            )

    except Exception as e:
        print(f"Error updating line manager ticket count: {e}")
