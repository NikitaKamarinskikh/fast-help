import os
from datetime import datetime
from data.config import distances
from math import radians, sqrt, sin, cos, atan2
from models import WorkersModel, OrdersModel


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


def worker_has_to_order_at_distance(worker: object, distance: int, order_distance: int):
    if order_distance < distance:
        return False

    if distance <= distances.short.meters:
        return True

    if distance <= distances.middle.meters:
        if worker.max_distance >= distances.middle.meters:
            if worker.orders_at_longer_distance_access_time >= datetime.now().timestamp():
                return True

    if distance <= distances.long.meters:
        if worker.max_distance == distances.long.meters:
            if worker.orders_at_longer_distance_access_time >= datetime.now().timestamp():  # Возможно нужно изменить
                return True

    return False


async def get_candidates_by_filters(order: object, excepted_user_telegram_id: int) -> list:
    workers = await WorkersModel.get_by_category_and_coordinates(
        category=[order.category],
        order_latitude=order.latitude,
        order_longitude=order.longitude,
        customer_telegram_id=excepted_user_telegram_id
    )
    candidates = list()
    order_distance_list = order.location.split()
    order_distance = (float(order_distance_list[0]), float(order_distance_list[1]))
    for worker in workers:
        worker_distance_list = worker.location.split()
        worker_distance = (float(worker_distance_list[0]), float(worker_distance_list[1]))
        distance = get_distance_between_two_points_in_meters(order_distance, worker_distance)
        if worker_has_to_order_at_distance(worker, distance, order.distance):
            setattr(worker, "distance", distance)
            candidates.append(worker)
    return candidates


async def get_orders_by_worker(worker: object, worker_location, max_distance: int = 500) -> list:
    worker_distance = (float(worker_location.latitude), float(worker_location.longitude))
    candidates = list()
    orders = await OrdersModel.get_not_completed_by_categories_and_coordinates(
        categories=worker.categories.all(),
        worker_latitude=int(worker_distance[0]),
        worker_longitude=int(worker_distance[1]),
        worker_telegram_id=worker.user.telegram_id
    )
    for order in orders:
        order_distance_list = order.location.split()
        order_distance = (float(order_distance_list[0]), float(order_distance_list[1]))
        distance = get_distance_between_two_points_in_meters(order_distance, worker_distance)
        if distance <= max_distance:
            setattr(order, "distance", distance)
            candidates.append(order)
    return candidates



