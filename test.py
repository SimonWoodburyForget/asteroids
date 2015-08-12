import random
import pyglet


from game import resources

window = pyglet.window.Window()
x = window.width/2
y = window.height/2


class S(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x = random.random() * 50

    def update(self, dt):
        self.x += self.velocity_x * dt

class C:
    def __init__(self, batch):
        self.batch = batch
        self.con = []


    def spawn(self, x, y, qty=3):

        for i in range(qty):

            sprite_this = S(
                img=resources.player_image,
                batch=self.batch)
            sprite_this.x = x
            sprite_this.y = y
            self.con.append(sprite_this)

    def update(self, dt):
        for i in self.con:
            i.update(dt)

main_batch = pyglet.graphics.Batch()
contain_this = C(main_batch)
contain_this.spawn(x, y)

@window.event
def on_draw():
    window.clear()
    main_batch.draw()


def update(dt):
    contain_this.update(dt)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
