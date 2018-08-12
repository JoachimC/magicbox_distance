from geopy import Point

from magicbox_distance import shapefile, distance, shapefile_convert

right_isosceles_triangle_start = Point(1.0, 1.0)
right_isosceles_triangle_middle = Point(1.1, 1.0)
right_isosceles_triangle_end = Point(1.1, 1.1)

right_isosceles_triangle_distance = distance.using_latitude_and_longitude(right_isosceles_triangle_start,
                                                                          right_isosceles_triangle_middle) + \
                                    distance.using_latitude_and_longitude(right_isosceles_triangle_middle,
                                                                          right_isosceles_triangle_end)


def create_right_isosceles_triangle(start, middle, end):
    parts = [shapefile.create_part(1, [start, middle, end])]
    return [shapefile.create_record(1, shapefile.ShapeType.POLYLINE, parts)]


def create_zero_distance(start):
    parts = [shapefile.create_part(1, [start, start])]
    return [shapefile.create_record(1, shapefile.ShapeType.POLYLINE, parts)]
