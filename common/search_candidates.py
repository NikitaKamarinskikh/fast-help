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


async def get_candidates_by_filters(order: object, excepted_users_telegram_ids: list) -> list:
    """
    return: [ {"worker": WorkerModelObject, "distance": int}, {"worker": WorkerModelObject, "distance": int} ]
    """
    # order_coordinates_str = order.location.split()
    # order_coordinates = (float(order_coordinates_str[0]), float(order_coordinates_str[1]))
    # worker_coordinates_list = worker.location.split()
    # worker_coordinates = (float(worker_coordinates_list[0]), float(worker_coordinates_list[1]))
    print("start getting users", datetime.now().time())
    workers = await WorkersModel.get_by_category(category=[order.category])
    # candidates = np.array(type(workers[0]))
    candidates = list()

    print("finish getting users", datetime.now().time())
    filename = f"{order.customer.user.telegram_id}_workers_coordinates.txt"
    # Запись координат в файл
    print("start searching", datetime.now().time())
    with open(filename, "w") as f:
        for worker in workers:
            f.write(f"{order.location} {worker.location} \n")
    print("finish wrinig data", datetime.now().time())
    # Эти координаты считает файл на си и записывает в другой файл
    print("start calculating coordinates data", datetime.now().time())
    os.system(f"./calc_distance {filename} result_{filename}")
    print("finish calculating coordinates data", datetime.now().time())
    f = open(f"result_{filename}", "r")

    print("start making candidates", datetime.now().time())
    for worker in workers:
        distance = int(f.readline())
        if distance <= 500: # and worker.user.telegram_id not in excepted_users_telegram_ids:
            setattr(worker, "distance", distance)
            candidates.append(worker)
    print("finish making candidates", datetime.now().time())
    print(len(candidates))
    f.close()
    os.remove(filename)
    os.remove(f"result_{filename}")
    print("finish searching", datetime.now().time())
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



