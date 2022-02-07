from models import WorkersModel
from geopy.distance import geodesic


def get_distance_between_two_points_in_meters(coordinates1: tuple, coordinates2: tuple) -> int:
    return round(geodesic(coordinates1, coordinates2).meters)


async def get_candidates_by_filters(category: object, coordinates: tuple) -> list:
    candidates = list()
    workers = await WorkersModel.get_by_filters(category=category)
    for worker in workers:
        worker_coordinates_list = worker.location.split()
        worker_coordinates = (float(worker_coordinates_list[0]), float(worker_coordinates_list[1]))
        if get_distance_between_two_points_in_meters(coordinates, worker_coordinates) == 500:
            candidates.append(worker)
    print(candidates)
    return candidates



