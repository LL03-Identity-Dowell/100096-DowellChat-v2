from datetime import datetime


def calculate_initial_waiting_time(ticket_count, waiting_time_per_ticket):
    return waiting_time_per_ticket * ticket_count

def update_waiting_times(queue, waiting_time_per_ticket):
    if queue:
        queue.sort(key=lambda x: datetime.fromisoformat(x['created_at'].replace('Z', '+00:00')))
        queue[0]['initial_waiting_time'] = 0
        for i in range(1, len(queue)):
            queue[i]['initial_waiting_time'] = waiting_time_per_ticket * i

