import os
from datetime import datetime
from math import radians, sqrt, sin, cos, atan2

from models import WorkersModel, OrdersModel
from geopy.distance import geodesic


def get_distance_between_two_points_in_meters(coordinates1: tuple, coordinates2: tuple) -> int:
    R = 6378.1

    lat1 = radians(coordinates1[0])
    lon1 = radians(coordinates1[1])
    lat2 = radians(coordinates2[0])
    lon2 = radians(coordinates2[1])

    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000
    return round(distance)


async def get_candidates_by_filters(order: object, excepted_user_telegram_id: int) -> list:
    workers = await WorkersModel.get_by_category(category=[order.category])
    candidates = list()
    filename = f"{order.customer.user.telegram_id}_workers_coordinates.txt"
    with open(filename, "w") as f:
        for worker in workers:
            f.write(f"{order.location} {worker.location} \n")
    os.system(f"./calc_distance {filename} result_{filename}")
    f = open(f"result_{filename}", "r")
    for worker in workers:
        distance = int(f.readline())
        if distance <= 500 and worker.user.telegram_id != excepted_user_telegram_id:
            setattr(worker, "distance", distance)
            candidates.append(worker)
    f.close()
    os.remove(filename)
    os.remove(f"result_{filename}")
    return candidates


async def get_orders_by_worker(worker: object, max_distance: int = 500) -> list:
    candidates = list()
    orders = await OrdersModel.get_not_completed_by_categories(worker.categories.all())
    filename = f"{worker.user.telegram_id}_order_coordinates.txt"
    worker_telegram_id = worker.user.telegram_id
    with open(filename, "w") as f:
        for order in orders:
            f.write(f"{worker.location} {order.location}\n")

    os.system(f"./calc_distance {filename} result_{filename}")

    f = open(f"result_{filename}", "r")
    for order in orders:
        distance = int(f.readline())
        if distance <= max_distance and order.customer.user.telegram_id != worker_telegram_id:
            setattr(order, "distance", distance)
            candidates.append(order)
    f.close()
    os.remove(filename)
    os.remove(f"result_{filename}")
    return candidates
