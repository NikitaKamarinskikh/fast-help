from math import radians, sqrt, sin, cos, atan2
from geopy.distance import geodesic as get_distance_between_two_cords_geo
# from common import get_city_by_coordinates


def get_distance_between_two_cords(lat1, lon1, lat2, lon2):
    R = 6378.1

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lon = lon2 - lon1
    delta_lat = lat2 - lat1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000
    return round(distance + 100)


if __name__ == '__main__':
    ...
    # print(get_distance_between_two_cords_geo((55.030199, 82.92043), (55.030199, 82.92043)).meters)
    #     # city = get_city_by_coordinates(54.983381, 82.805789)
    #     #
    print(get_distance_between_two_cords_geo( (54.980394, 82.897891), (54.983357, 82.805794)).meters )
    # print(get_distance_between_two_cords(55.030199, 82.33333, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.123, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.123, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92123043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.345345, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.123123, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.42534534, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.345345, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.030199, 82.92043))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
    # print(get_distance_between_two_cords(55.030199, 82.32403405, 55.753215, 37.34534534))
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.030199, 82.92043))
    #

