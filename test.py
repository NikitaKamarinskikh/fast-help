import math
from geopy.distance import geodesic as get_distance_between_two_cords
from common import get_city_by_coordinates
# def get_distance_between_two_cords(lat1, lon1, lat2, lon2):
#     R = 6378.1
#
#     lat1 = math.radians(lat1)
#     lon1 = math.radians(lon1)
#     lat2 = math.radians(lat2)
#     lon2 = math.radians(lon2)
#
#     delta_lon = lon2 - lon1
#     delta_lat = lat2 - lat1
#
#     a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     distance = R * c * 1000
#     return distance


if __name__ == '__main__':
    #print(get_distance_between_two_cords((55.030199, 82.92043), (55.030199, 82.92043)).meters)
    city = get_city_by_coordinates(54.983381, 82.805789)
    print(city)
    # print(get_distance_between_two_cords(55.030199, 82.92043, 55.753215, 37.622504))
