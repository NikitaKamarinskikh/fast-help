import csv


def get_city_by_coordinates(lat: float, lon: float) -> str:
    city: str = "Неизвестный"
    with open("common/cities.csv") as file:
        reader = csv.reader(file)
        for row in reader:  # row = [Город, Регион, Федеральный округ, lat, lng]
            if len(row) == 5:
                file_city, file_lat, file_lon = row[0], float(row[3]), float(row[4])
                if round(file_lat) == round(lat) and round(file_lon) == round(lon):
                    return row[1]
            else:
                file_city, file_lat, file_lon = row[0], float(row[2]), float(row[3])
                if file_lat == lat and file_lon == lon:
                    return row[1]
    return city


