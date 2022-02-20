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
    orders = await OrdersModel.get_not_completed_by_categories(worker.categories.all())
    for order in orders:
        order_coordinates_list = order.location.split()
        order_coordinates = (float(order_coordinates_list[0]), float(order_coordinates_list[1]))
        distance = get_distance_between_two_points_in_meters(order_coordinates, worker_coordinates)
        if distance <= max_distance:
            setattr(order, "distance", distance)
            candidates.append(order)
    return candidates



