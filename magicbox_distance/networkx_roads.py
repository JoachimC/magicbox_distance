# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf

ID_KEY = "id"
START_KEY = "start"
END_KEY = "end"
DISTANCE_KEY = "distance"


def create_node_id(node):
    return "{lat:+f}{lon:+f}".format(lat=node.latitude, lon=node.longitude)


def create_road_id(start, end):
    return "{start} to {end}".format(start=create_node_id(start), end=create_node_id(end))
