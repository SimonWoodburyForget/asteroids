import random


# might not want to load sprites here
from pyglet.sprite import Sprite
from . import resources






class Particle(Sprite):
    '''Base class for a particle'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velovity_x = 0
        self.velocity_y = 0
        self.rotation_speed = random.random() * 70

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rotation += self.rotation_speed * dt


class Dust():
    '''Particles to be tied with asteroids'''
    def __init__(self, batch):
        self.batch = batch
        self.particles = []

    def spawn(self, pos, vel, qty=3):

        for count in range(qty):

            particle = Particle(img=random.choice(resources.asteroid_particles),
                                batch=self.batch)
            particle.x = pos[0] + random.random()
            particle.y = pos[1] + random.random()
            particle.velocity_x = vel[0] + random.random()
            particle.velocity_y = vel[1] + random.random()

            self.particles.append(particle)


    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
