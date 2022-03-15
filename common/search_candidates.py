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

    print("middle distance check")
    if distance <= distances.middle.meters:
        print("middle")
        if worker.max_distance >= distances.middle.meters:
            print("meters check")
            if worker.orders_at_longer_distance_access_time >= datetime.now().timestamp():
                print("time check")
                return True

    if distance <= distances.long.meters:
        if worker.max_distance == distances.long.meters:
            if worker.orders_at_longer_distance_access_time >= datetime.now().timestamp():  # Возможно нужно изменить
                return True

    return False


async def get_candidates_by_filters(order: object, excepted_user_telegram_id: int) -> list:
    workers = await WorkersModel.get_by_category(category=[order.category])
    candidates = list()
    order_distance_list = order.location.split()
    order_distance = (float(order_distance_list[0]), float(order_distance_list[1]))
    # filename = f"{order.customer_telegram_id}_workers_coordinates.txt"
    # with open(filename, "w") as f:
    #     for worker in workers:
    #         f.write(f"{order.location} {worker.location} \n")
    # code = os.system(f"./calc_distance {filename} result_{filename}")
    # print(code)
    # # code = subprocess.call(f"./calc_distance {filename} result_{filename}")
    # f = open(f"result_{filename}", "r")
    excepted_user_telegram_id = str(excepted_user_telegram_id)
    for worker in workers:
        # distance = int(f.readline())
        worker_distance_list = worker.location.split()
        worker_distance = (float(worker_distance_list[0]), float(worker_distance_list[1]))
        distance = get_distance_between_two_points_in_meters(order_distance, worker_distance)
        print(distance, order.distance)
        if worker_has_to_order_at_distance(worker, distance, order.distance):
        # if distance <= order.distance: # and worker.telegram_id != excepted_user_telegram_id:
            setattr(worker, "distance", distance)
            candidates.append(worker)
    # f.close()
    # os.remove(filename)
    # os.remove(f"result_{filename}")
    return candidates


async def get_orders_by_worker(worker: object, max_distance: int = 500) -> list:
    candidates = list()
    orders = await OrdersModel.get_not_completed_by_categories(worker.categories.all())
    # filename = f"{worker.user.telegram_id}_order_coordinates.txt"
    # worker_telegram_id = int(worker.user.telegram_id)
    # with open(filename, "w") as f:
    #     for order in orders:
    #         f.write(f"{worker.location} {order.location}\n")

    # code = subprocess.call(f"./calc_distance {filename} result_{filename}")
    # code = os.system(f"./calc_distance {filename} result_{filename}")
    # f = open(f"result_{filename}", "r")
    # print("start loop", datetime.now())
    worker_distance_list = worker.location.split()
    worker_distance = (float(worker_distance_list[0]), float(worker_distance_list[1]))
    for order in orders:
        # distance = int(f.readline())
        order_distance_list = order.location.split()
        order_distance = (float(order_distance_list[0]), float(order_distance_list[1]))
        distance = get_distance_between_two_points_in_meters(order_distance, worker_distance)
        if distance <= max_distance: # and int(order.customer_telegram_id) != worker_telegram_id:
            setattr(order, "distance", distance)
            candidates.append(order)
    # f.close()
    # os.remove(filename)
    # os.remove(f"result_{filename}")
    # print("data found", datetime.now())
    return candidates



