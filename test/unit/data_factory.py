from geopy import Point

from magicbox_distance import shapefile, distance

right_angle_start = Point(1.0, 1.0)
right_angle_middle = Point(1.1, 1.0)
right_angle_end = Point(1.1, 1.1)

right_angle_distance = distance.using_latitude_and_longitude(right_angle_start, right_angle_middle) + \
                       distance.using_latitude_and_longitude(right_angle_middle, right_angle_end)


def create_shapefile(roads):
    return [shapefile.create_record(index, shapefile.ShapeType.POLYLINE, [road]) for index, road in enumerate(roads)]

def create_part(*args):
    return shapefile.create_part(1, list(args))
