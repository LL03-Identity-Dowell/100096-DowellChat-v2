from datetime import datetime

def calculate_initial_waiting_time(ticket_count, waiting_time):
    return waiting_time * ticket_count

def convert_timestamp(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y_%m_%d")

def fetch_data_for_collection(data_cube, api_key, db_name, coll_name, line_manager):
    response = data_cube.fetch_data(
        api_key=api_key,
        db_name=db_name,
        coll_name=coll_name,
        filters={'is_closed': False, 'line_manager': line_manager},
        limit=100,
        offset=0
    )
    return response['data'] if response['data'] else []

# def update_waiting_times(workspace_id, api_key, product, line_manager):
#     data_cube = DataCubeConnection()

#     waiting_time_db_name = f"{workspace_id}_cs_ticketing_system_db0"
#     waiting_time_coll_name = f"{workspace_id}_setting"
    
#     waiting_time_response = data_cube.fetch_data(
#         api_key=api_key, db_name=waiting_time_db_name, coll_name=waiting_time_coll_name, filters={}, limit=1, offset=0)
    
#     waiting_time_per_ticket = int(waiting_time_response['data'][0]['waiting_time'])
#     db_name = map_product_to_db(workspace_id, api_key, product)
#     collections = get_database_collections(api_key, db_name)[:7]

#     queue = []
#     with ThreadPoolExecutor() as executor:
#         future_to_coll_name = {executor.submit(fetch_data_for_collection, data_cube, api_key, db_name, coll_name, line_manager): coll_name for coll_name in collections}
#         for future in as_completed(future_to_coll_name):
#             try:
#                 data = future.result()
#                 queue.extend(data)
#             except Exception as e:
#                 print(f"Error fetching data for collection {future_to_coll_name[future]}: {e}")

#     if queue:
#         queue.sort(key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '+00:00')))

#         updates = []
#         for i, ticket in enumerate(queue):
#             converted_timestamp = convert_timestamp(ticket['created_at'])
#             ticket_col = None
#             for coll_name in collections:
#                 if converted_timestamp in coll_name:
#                     ticket_col = coll_name
#                     break
            
#             if not ticket_col:
#                 print(f"No collection found for ticket ID: {ticket['_id']} with timestamp: {converted_timestamp}")
#                 continue

#             ticket_waiting_time = waiting_time_per_ticket * i if i > 0 else 0
#             updates.append({
#                 'api_key': api_key,
#                 'db_name': db_name,
#                 'coll_name': ticket_col,
#                 'query': {'_id': ticket['_id']},
#                 'update_data': {"waiting_time": ticket_waiting_time}
#             })
#             print(f"Ticket ID: {ticket['_id']}, Waiting Time: {ticket_waiting_time} minutes, Collection: {ticket_col}")

#         for update in updates:
#             try:
#                 data_cube.update_data(**update)
#             except Exception as e:
#                 print(f"Error updating ticket {update['query']['_id']}: {e}")

#         print("Waiting times updated successfully.")

# Example usage
# update_waiting_times('workspace_id', 'api_key', 'product', 'line_manager')





# update_waiting_times(
#     workspace_id="63cf89a0dcc2a171957b290b",
#     api_key="1b834e07-c68b-4bf6-96dd-ab7cdc62f07f",
#     product="test_product",
#     line_manager="Abate"
# )