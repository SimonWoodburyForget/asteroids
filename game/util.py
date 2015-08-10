import math

import pyglet

def center_image(image):
    """Sets an images anchor point to its center"""
    if type(image) == type([]):
        for i in image:
            i.anchor_x = i.width/2
            i.anchor_y = i.height/2
    else:
        image.anchor_x = image.width/2
        image.anchor_y = image.height/2

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt(
        (point_1[0] - point_2[0]) ** 2 +
        (point_1[1] - point_2[1]) ** 2
    )
