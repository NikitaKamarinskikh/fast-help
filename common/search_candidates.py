import os
from datetime import datetime

from models import WorkersModel, OrdersModel
from geopy.distance import geodesic


def get_distance_between_two_points_in_meters(coordinates1: tuple, coordinates2: tuple) -> int:
    try:
        return int(geodesic(coordinates1, coordinates2).meters)
    except Exception as e:
        print(e)
        return 1000000


async def get_candidates_by_filters(category: object, coordinates: tuple, excepted_users_telegram_ids: list) -> list:
    """
    return: [ {"worker": WorkerModelObject, "distance": int}, {"worker": WorkerModelObject, "distance": int} ]
    """
    candidates = list()
    workers = await WorkersModel.get_by_category(category=category)
    for worker in workers:
        worker_coordinates_list = worker.location.split()
        worker_coordinates = (float(worker_coordinates_list[0]), float(worker_coordinates_list[1]))
        distance = get_distance_between_two_points_in_meters(coordinates, worker_coordinates)
        if distance <= 500 and worker.user.telegram_id not in excepted_users_telegram_ids:
            candidates.append({
                "worker": worker,
                "distance": distance
            })
    return candidates


async def get_orders_by_worker(worker: object, max_distance: int = 500) -> list:
    candidates = list()
    worker_coordinates_list = worker.location.split()
    worker_coordinates = (float(worker_coordinates_list[0]), float(worker_coordinates_list[1]))
    print("start_getting_orders", datetime.now().time())
    orders = await OrdersModel.get_not_completed_by_categories(worker.categories.all())
    print("finish_getting_orders", datetime.now().time())
    print()

    print("start calculating", datetime.now().time())
    filename = f"{worker.user.telegram_id}_order_coordinates.txt"

    # Вывод координат в файл
    with open(filename, "w") as f:
        for order in orders:
            # order_coordinates_list = order.location.split()
            # order_coordinates = (float(order_coordinates_list[0]), float(order_coordinates_list[1]))
            # distance = get_distance_between_two_points_in_meters(order_coordinates, worker_coordinates)
            # if distance <= max_distance:
            #     setattr(order, "distance", distance)
            #     candidates.append(order)

            f.write(f"{worker.location} {order.location}\n")

    # Эти координаты считает файл на си и записывает в другой файл
    os.system(f"./calc_distance {filename} result_{filename}")

    # Затем открываем новый файл и проверяем числа еще раз
    f = open(f"result_{filename}", "r")
    for order in orders:
        distance = int(f.readline())
        if distance <= max_distance:
            setattr(order, "distance", distance)
            candidates.append(order)
    f.close()
    os.remove(filename)
    os.remove(f"result_{filename}")
    print(len(candidates))
    print("finish calculating", datetime.now().time())
    print()
    return candidates



