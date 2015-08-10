import random

from . import resources
from . import physicalobject

class Asteroid(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        img = random.choice(resources.asteroid_images)
        super().__init__(img=img, *args, **kwargs)

        self.scale *= 1.0
        self.rotation_speed = random.random() * 70
        self.score_dif = 10

    def handle_collision_with(self, other_object):
        super().handle_collision_with(other_object)

        if self.dead and self.scale > 0.25:
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):

                new_asteroid = Asteroid(self.screen_bounds,
                                    x=self.x, y=self.y, batch=self.batch
                )
                new_asteroid.rotation = random.randint(0, 360)

                new_asteroid.velocity_x = (
                    random.random() * -70 + self.velocity_x
                )
                new_asteroid.velocity_y = (
                    random.random() * 70 - self.velocity_y
                )
                new_asteroid.scale = self.scale * 0.5

                self.new_objects.append(new_asteroid)


    def update(self, dt):
        super().update(dt)
        self.rotation += self.rotation_speed * dt
