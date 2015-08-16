from pyglet.sprite import Sprite

from . import util

class PhysicalObject(Sprite):
    """Basic physic object, used for objects that require physical interaction.

    This object has velocity, rotation speed, will check for screen bounts to
    warp around once it goes off screen, is able to create new particles and
    objects by simple appending the objects to it's lists"""
    def __init__(self, screen_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_size = screen_size

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.reacts_to_bullets = True
        self.is_bullet = False

        self.dead = False
        self.invulnerable = False

        ## Lists used to requests more new objects
        # new physical objects will be thrown into collition checks
        self.new_objects = []
        # new particles objects will be only require
        # to be updated by it's wrapper class
        self.new_particles = []

        # lists of handlers to be pushed to the window object
        self.event_handlers = []

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        """Physical objects will wrap around the screen"""
        min_x = -self.image.width/2
        min_y = -self.image.height/2

        max_x = self.screen_size[0] + self.image.width/2
        max_y = self.screen_size[1] + self.image.height/2

        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):
        """Checks if it can collide with the other object"""
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False

        # Every object is a circle with a radius of the image width.
        collision_distance = (self.image.width/2 * self.scale +
                    other_object.image.width/2 * other_object.scale)
        actual_distance = util.distance(self.position,
                    other_object.position)

        return (actual_distance <= collision_distance)


    def handle_collision_with(self, other_object):
        """Collides with the other object"""
        if type(self) == type(other_object):
            self.dead = False
        elif self.invulnerable:
            self.dead = False
        else:
            self.dead = True

            # Simulates momentum
            self.velocity_x += other_object.velocity_x/25
            self.velocity_y -= other_object.velocity_y/25

    """event handled by pushing it to the window object"""
    def on_resize(self, width, height):
        self.screen_size = (width, height)
        self.check_bounds()
