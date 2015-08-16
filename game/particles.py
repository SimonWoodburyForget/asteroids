import random


# might not want to load sprites here
from pyglet.sprite import Sprite
from . import resources
import pyglet


# No exact idea of the efficiency of using sprites here.
class Particle(Sprite):
    """Basic particle object, used for small objects that don't
    require any physical interaction

    This object will have velocity, rotation speed, and a certain random
    life time, will check for screen bounts to die off screen"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velovity_x = 0
        self.velocity_y = 0
        self.rotation_speed = random.random() * 70

        # seconds to particle to die, will randomly die off over ~1 minute
        self.life_time = random.random() * 25
        self.dead = False

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rotation += self.rotation_speed * dt
        self.check_bounds()

        self.life_time -= dt
        if self.life_time < 0: self.dead = True

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


class Dust():
    """Particles wrapper, will manage all particles"""
    def __init__(self, screen_size, batch):
        self.screen_size = screen_size
        self.batch = batch
        self.particles = []


    def spawn(self, pos, vel, scale, qty=10):
        """Spawns particles,
            pos = spawn position
            vel = velocity of particles
            scale = size of particles
            qty = amount of particles

        Particles will spawn in a random area around the position
        then will diviate a random amount of velocity from each other.
        """
        for count in range(qty):

            particle = Particle(img=resources.asteroid_particles,
                                batch=self.batch)

            # spawn area, scale used to change per size of asteroids
            particle.x = pos[0] - random.random() * 50.0 * scale
            particle.y = pos[1] - random.random() * 50.0 * scale

            # takes the velocity of other object * 1.5 to get off screen faster
            particle.velocity_x = vel[0] * random.random() * 1.5
            particle.velocity_y = vel[1] * random.random() * 1.5

            particle.screen_size = self.screen_size
            particle.scale = 1

            self.particles.append(particle)


    def update(self, dt):
        """Used to update the position of every particle"""
        to_remove = []
        for particle in self.particles:
            particle.update(dt)
            particle.screen_size = self.screen_size
            if particle.dead:
                to_remove.append(particle)

        for remove in to_remove:
            self.particles.remove(remove)
            remove.delete()
