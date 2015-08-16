import pyglet
from pyglet.window import key

import platform
platform_ = platform.platform()
platform.release()
platform.version()

try:
    if platform_.split('-')[6] in ['LinuxMint']:
        # fix's sound related issues on linux mint caused by PulseAudio, like:
        # Segmentation Faults - Premature sound cutting - too large exception
        pyglet.options['audio'] = ('openal', 'silent')
except:
    pass

from game import player
from game import load
from game import guiobject

# To make everything but bullets make explosions sounds
from game.resources import explosion_sound
from game.bullet import Bullet

from game.asteroid import Asteroid


screen_width = 1366
screen_height = 768
FPS = 120.0

def main():
    game = GameWindow(screen_width, screen_height, resizable=True)
    pyglet.clock.schedule_interval(game.update, 1/FPS)
    pyglet.app.run()


class GameWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        # load and set default config here
        super().__init__(*args, **kwargs)

        self._spawn = 0
        self._score = 0

        self.gui_batch = pyglet.graphics.Batch()
        self.hud = guiobject.HudObjects(self.screen_size, self.gui_batch)
        self.push_handlers(self.hud)



        self.game_over = guiobject.Selection(
            'GameOver',
            self.screen_size,
            batch=self.gui_batch)
        self.game_over.insert('Restart', self.reset_game)
        self.game_over.insert('Exit', self.exit_game)
        self.game_over.auto_call(self.save_score)
        self.push_handlers(self.game_over)

        self.menu = guiobject.Selection(
            'Menu',
            self.screen_size,
            batch=self.gui_batch)
        self.menu.insert('Restart', self.reset_game)
        self.menu.insert('Exit', self.exit_game)
        self.menu.auto_call(self.save_score)
        self.push_handlers(self.menu)

        

        self.game_batch = pyglet.graphics.Batch()
        self.physical_objects = []
        self._event_stack_size = 0

        self.reset_game()

    @property
    def screen_size(self):
        return (self.width, self.height)

    def on_draw(self):
        self.clear()
        self.game_batch.draw()
        self.gui_batch.draw()



    def reset_game(self):

        _scores = load.scores(self._score)
        self._top_score = sorted(_scores, key=lambda k: k['score'])[-1]['score']
        self.hud.top_score = self._top_score

        # destroy gane objects
        while self._event_stack_size > 0:
            self.pop_handlers()
            self._event_stack_size -= 1

        for obj in self.physical_objects:
            obj.delete()

        self.spawn_condition = 3
        self.asteroids_remaining = 0

        self._lives = 4
        self.hud.lives = self._lives
        
        self._score = 0
        self.hud.score = self._score

        self._spawn = 0

        self.physical_objects = []
        self.particles = []

        self.player_ship = player.Player(
            screen_size=(self.width,
                         self.height),
            x=self.width/2,
            y=self.height/2,
            batch=self.game_batch
        )
        self.physical_objects.append(self.player_ship)
        # load game evnet handlers
        for obj in self.physical_objects:
            for handler in obj.event_handlers:
                self.push_handlers(handler)
                self._event_stack_size += 1

    def next_spawn(self):
        """spawn next wave adding dificulty and keeping the game going"""
        self._spawn += 1
        self.hud.spawn = self._spawn

        # lets use fibonacci
        a, b = 0, 1
        for i in range(0, self._spawn):
            a, b = b, a + b
        num_asteroids = a

        asteroids = load.asteroids(
            num_asteroids,
            self.player_ship.position,
            (self.width, self.height),
            batch=self.game_batch)
        self._event_stack_size += len([self.push_handlers(x) for x in asteroids])

        self.physical_objects += asteroids


        self.spawn_condition 
        if self._spawn <= 2:
            self.spawn_condition = num_asteroids
        elif self._spawn >= 3:
            self.spawn_condition = num_asteroids -1

    def update(self, dt):

        # game physics/mechanics
        if not self.menu.visible:
            """Checking collision with objects"""
            for i in range(len(self.physical_objects)):
                for j in range(i+1, len(self.physical_objects)):
                    obj_1 = self.physical_objects[i]
                    obj_2 = self.physical_objects[j]

                    if not obj_1.dead and not obj_2.dead:
                        if obj_1.collides_with(obj_2):
                            obj_1.handle_collision_with(obj_2)
                            obj_2.handle_collision_with(obj_1)

            """Checking requests to_add objects"""
            to_add = []
            for obj in self.physical_objects:
                obj.update(dt)
                to_add.extend(obj.new_objects)
                obj.new_objects = []

                self.particles += obj.new_particles

            """Checking players life state"""
            if self.player_ship.dead:
                if self._lives:
                    self._lives -= 1
                    self.hud.lives = self._lives
                    self.player_ship.dead = False
                    self.player_ship.set_invulnerable()
                else:
                    self.game_over.set_visible()


            """Removing requested to_remove objects"""
            for to_remove in [obj for obj
                                  in self.physical_objects
                                  if obj.dead]:
                """Calculating Score (in/de)crement"""
                self._score += to_remove.score_dif
                self.hud.score = self._score
                if self._score > self._top_score:
                    self._top_score = self._score
                    self.hud.top_score = self._top_score

                """Removing object"""
                to_remove.delete()
                self.physical_objects.remove(to_remove)
                if not isinstance(to_remove, Bullet):
                    explosion_sound.play()

            """Adding requested objects"""
            self.physical_objects.extend(to_add)

            """Updating physical objects"""
            self.asteroids_remaining = 0
            for obj in self.physical_objects:
                obj.update(dt)

                """Counting asteroids"""
                if isinstance(obj, Asteroid):
                    self.asteroids_remaining += 1

            """Spawning more asteroids"""
            if self.asteroids_remaining < self.spawn_condition:
                self.next_spawn()

            for part in self.particles:
                part.update(dt)


    def on_key_press(self, symbol, modifiers):

        if symbol == key.ESCAPE:
            if self.menu.visible:
                self.menu.set_invisible()
                #options.set_invisible()
                return True
            else:
                if self.game_over.visible:
                    self.game_over.set_invisible()
                self.menu.set_visible()
                return True

    def exit_game(self):
        self.save_score()
        exit()

    def save_score(self):
        load.scores(self._score)




if __name__ == '__main__':
    main()
