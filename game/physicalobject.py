from pyglet.sprite import Sprite

from . import util

class PhysicalObject(Sprite):

    def __init__(self, screen_size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.screen_size = screen_size

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.reacts_to_bullets = True
        self.is_bullet = False

        self.dead = False
        self.new_objects = []
        self.new_particles = []

        self.event_handlers = []

        self.invulnerable = False

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def on_resize(self, width, height):
        self.screen_size = (width, height)
        self.check_bounds()

    def check_bounds(self):
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
        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False

        collision_distance = (self.image.width/2 * self.scale +
                    other_object.image.width/2 * other_object.scale)
        actual_distance = util.distance(self.position,
                    other_object.position)

        return (actual_distance <= collision_distance)


    def handle_collision_with(self, other_object):
        if type(self) == type(other_object):
            self.dead = False
        elif self.invulnerable:
            self.dead = False
        else:
            self.dead = True
            self.velocity_x += other_object.velocity_x/25
            self.velocity_y -= other_object.velocity_y/25
