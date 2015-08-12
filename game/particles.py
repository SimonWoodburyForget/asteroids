import random


# might not want to load sprites here
from pyglet.sprite import Sprite
from . import resources
import pyglet





class Particle(Sprite):
    '''Base class for a particle'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velovity_x = 0
        self.velocity_y = 0
        self.rotation_speed = random.random() * 70
        self.dead = False

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rotation += self.rotation_speed * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = -self.image.width/2
        min_y = -self.image.height/2

        max_x = self.screen_size[0] + self.image.width/2
        max_y = self.screen_size[1] + self.image.height/2
        if self.x < min_x:
            self.dead = True
        elif self.x > max_x:
            self.dead = True
        if self.y < min_y:
            self.dead = True
        elif self.y > max_y:
            self.dead = True


class Rocks():
    '''Particles to be tied with asteroids'''
    def __init__(self, screen_size, batch):
        self.screen_size = screen_size
        self.batch = batch
        self.particles = []

    #    self._re()

    #def _re(self):
        #pyglet.clock.schedule_once(self._re, 6)


    def spawn(self, pos, vel, qty=3):

        for count in range(qty):

            particle = Particle(img=random.choice(resources.asteroid_particles),
                                batch=self.batch)
            particle.x = pos[0] + random.random() * 50
            particle.y = pos[1] + random.random() * 50
            particle.velocity_x = vel[0] + random.random() * 50
            particle.velocity_y = vel[1] + random.random() * 50
            particle.screen_size = self.screen_size

            self.particles.append(particle)


    def update(self, dt):
        to_remove = []
        for particle in self.particles:
            particle.update(dt)
            particle.screen_size = self.screen_size
            if particle.dead:
                to_remove.append(particle)

        for remove in to_remove:
            self.particles.remove(remove)
            remove.delete()
