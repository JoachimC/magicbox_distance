from magicbox_distance import shapefile, distance, shapefile_convert

right_isosceles_triangle_start = shapefile.create_point(1.0, 1.0)
right_isosceles_triangle_middle = shapefile.create_point(1.1, 1.0)
right_isosceles_triangle_end = shapefile.create_point(1.1, 1.1)

start_tuple = shapefile_convert.to_tuple(right_isosceles_triangle_start)
middle_tuple = shapefile_convert.to_tuple(right_isosceles_triangle_middle)
end_tuple = shapefile_convert.to_tuple(right_isosceles_triangle_end)

right_isosceles_triangle_distance = distance.using_latitude_and_longitude_in_km(start_tuple, middle_tuple) + \
                                    distance.using_latitude_and_longitude_in_km(middle_tuple, end_tuple)


def create_right_isosceles_triangle(start, middle, end):
    parts = [shapefile.create_part(1, [start, middle, end])]
    return [shapefile.create_record(1, shapefile.ShapeType.POLYLINE, parts)]


def create_zero_distance(start):
    parts = [shapefile.create_part(1, [start, start])]
    return [shapefile.create_record(1, shapefile.ShapeType.POLYLINE, parts)]
