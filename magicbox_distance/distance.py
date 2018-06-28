from geopy.distance import great_circle

def using_latitude_and_longitude(first, second):
    return great_circle(first, second).kilometers
