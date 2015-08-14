import random
import math
import json
import time

import pyglet
from pyglet.graphics import OrderedGroup

from . import guiobject
from . import resources
from . import physicalobject as po
from . import asteroid
from .util import distance


def asteroids(num_asteroids, player_position, screen_size, batch):
    """Creates a list of sprites to draw asteroids,
        making sure they aren't on top of the player"""
    asteroids = []
    for i in range(num_asteroids):

        asteroid_x, asteroid_y = player_position
        while distance((asteroid_x, asteroid_y), player_position) < 100:
            asteroid_x = random.randint(0, screen_size[0])
            asteroid_y = random.randint(0, screen_size[1])

        new_asteroid = asteroid.Asteroid(screen_size=screen_size,
                                    x=asteroid_x, y=asteroid_y, batch=batch)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x = random.random() * 40
        new_asteroid.velocity_y = random.random() * 40
        asteroids.append(new_asteroid)

    return asteroids


def player_lives(screen_size, num_icons, batch):
    """Creates a list of sprites to draw amount of player lives."""
    player_lives = []
    for i in range(num_icons):
        x = screen_size[0] - 25 - i * 30
        y = screen_size[1] - 25

        new_sprite = pyglet.sprite.Sprite(img=resources.player_image,
            x=x, y=y, batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)

    return player_lives

def scores(score=None):
    """Reads, appends, and returns scores

    Leaving no score argument will return current score
    Entering score argument will return updated score

    Doesn't save score if 0
    """

    with open('./data/score.json', 'r') as stream:
        score_data = json.load(stream)

    if score not in (0, None):
        # adding score
        data = {'score':score, 'date':time.time()}

        if score_data:
            # data exists
            score_data.append(data)

        else:
            # data doesn't exist
            score_data = [data]

    if score_data:
        with open('./data/score.json', 'w') as stream:
            stream.write(json.dumps(score_data))
        
        return score_data

    else:
        return [{'date':0, 'score':0}]
