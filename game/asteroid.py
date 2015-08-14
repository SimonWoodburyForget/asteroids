import random

from . import resources
from . import physicalobject
from . import particles

class Asteroid(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        img = random.choice(resources.asteroid_images)
        super().__init__(img=img, *args, **kwargs)

        self.scale *= 1.0
        self.rotation_speed = random.random() * 70
        self.score_dif = 10


    def handle_collision_with(self, other_object):
        super().handle_collision_with(other_object)

        self.new_particles = []
        if self.dead:
            self.dust = particles.Dust(self.screen_size, self.batch)
            vel = (other_object.velocity_x, other_object.velocity_y)
            pos = (self.x, self.y)
            self.dust.spawn(pos, vel, self.scale)
            self.new_particles.append(self.dust)

        if self.dead and self.scale > 0.25:
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):

                new_asteroid = Asteroid(self.screen_size,
                                    x=self.x, y=self.y, batch=self.batch)
                new_asteroid.rotation = random.randint(0, 360)
                new_asteroid.velocity_x = (
                    random.random() * -70 + self.velocity_x)
                new_asteroid.velocity_y = (
                    random.random() * 70 - self.velocity_y)
                new_asteroid.scale = self.scale * 0.5

                self.new_objects.append(new_asteroid)



    def update(self, dt):
        super().update(dt)
        self.rotation += self.rotation_speed * dt

    def delete(self):
        super().delete()
