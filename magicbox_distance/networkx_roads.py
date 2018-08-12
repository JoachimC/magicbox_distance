# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf

ID_KEY = "id"
START_ID_KEY = "start_id"
END_ID_KEY = "end_id"
START_KEY = "start"
END_KEY = "end"
DISTANCE_KEY = "distance"


def create_node_id(node):
    return "{latitude:+f},{longitude:+f}".format(latitude=node.latitude, longitude=node.longitude)


def create_road_id_from_node_ids(start_node_id, end_node_id):
    return "{start} to {end}".format(start=start_node_id, end=end_node_id)


def create_road_id_from_points(start, end):
    return create_road_id_from_node_ids(create_node_id(start), create_node_id(end))
