import pyglet
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import OrderedGroup
from pyglet.window import key

from .resources import menu_background
from . import resources


class HudObjects:
    """Hud objects are game stats that are displayed and updated while playing
    the game, this keeps track of there current state

    Should not understand game mechanics else then there current on going state
    """
    def __init__(self, screen_size, batch):
        self.screen_size = screen_size
        self.batch = batch

        self._player_lives = []

        self._score_label = Label(batch=self.batch)
        self._score_text = 'Score: {}'
        self._score = 0

        self._top_score_label = Label(batch=self.batch)
        self._top_score_text = 'Top Score: {}'
        self._top_score = 0

        self._spawn_label = Label(batch=self.batch)
        self._spawn_label.anchor_x = 'center'
        self._spawn_text = 'Spawn: {}'
        self._spawn = 0


    @property
    def lives(self):
        for c, i in enumerate(self._player_lives):
            i.x = self.width - 25 - c * 30
            i.y = self.height - 25

        return self._player_lives
    @lives.setter
    def lives(self, lives):
        for _ in range(lives+1):
            if len(self._player_lives) > lives:
                life = self._player_lives.pop()
                life.delete()
            elif len(self._player_lives) < lives:
                life = pyglet.sprite.Sprite(img=resources.player_image,
                                                    batch=self.batch)
                life.scale = 0.5
                self._player_lives.append(life)
        return self.lives


    @property
    def score(self):
        text = self._score_text.format(self._score)
        self._score_label.text = text
        self._score_label.x = 10
        self._score_label.y = self.height - 25
        return self._score_label
    @score.setter
    def score(self, score):
        self._score = score
        return self.score


    @property
    def top_score(self):
        text = self._top_score_text.format(self._top_score)
        self._top_score_label.text = text
        self._top_score_label.x = 10
        self._top_score_label.y = self.height - 50
        return self._top_score_label
    @top_score.setter
    def top_score(self, top_score):
        self._top_score = top_score
        return self.top_score


    @property
    def spawn(self):
        text = self._spawn_text.format(self._spawn)
        self._spawn_label.text = text
        self._spawn_label.x = self.width / 2
        self._spawn_label.y = self.height - 25
        return self._spawn_label
    @spawn.setter
    def spawn(self, spawn):
        self._spawn = spawn
        return self.spawn


    @property
    def width(self):
        return self.screen_size[0]
    @width.setter
    def width(self, value):
        self.screen_size = (value, self.width)


    @property
    def height(self):
        return self.screen_size[1]
    @height.setter
    def height(self):
        self.screen_size = (self.width, value)


    def on_resize(self, width, height):
        self.screen_size = (width, height)
        self.score
        self.top_score
        self.spawn
        self.lives



class Selection(Sprite):
    """Basic class to create menu, with buttons, and functions when pressed"""
    def __init__(self, name, screen_size, *args, **kwargs):
        x = screen_size[0]/2
        y = screen_size[1]/2
        super().__init__(img=menu_background, x=x, y=y,
            group=OrderedGroup(0), *args, **kwargs)
        self.name = name
        self.visible = False

        # called when set visible
        self._auto_calls = []

        self.names = []
        self.buttons = []
        self.calls = []
        self.selector = 0

        self.name_label = Label(
            anchor_x='center',
            batch=self.batch,
            group=OrderedGroup(1)
        )
        self._position_name

    def auto_call(self, call):
        '''Originally made to save the game on game over and menu open'''
        self._auto_calls.append(call)

    def on_resize(self, width, height):
        self.x = width/2
        self.y = height/2

        self._position_name()
        self._position_buttons()

    def _position_name(self):
        self.name_label.x = self.x
        self.name_label.y = self.y + self.image.height/2 - 30

    def _position_buttons(self):
        _x = self.x
        _y = self.y + self.image.height/2 - 70
        for count, button in enumerate(self.buttons):
            button.x = _x
            button.y = _y - count * 20


    def insert(self, name, call):
        button = Label(
            anchor_x='center',
            batch=self.batch,
            group=OrderedGroup(1)
        )
        self.names.append(name)
        self.buttons.append(button)
        self.calls.append(call)

        self._position_buttons()


    def set_visible(self):
        if not self.visible: # game window seems to call this on repeat,
                             # temporary fix to avoid saving score over it self.

            for call in self._auto_calls:
                call()
            self.visible = True
            self.name_label.text = self.name
            self._reload_buttons()

    def set_invisible(self):
        self.visible = False
        self.selector = 0
        self.name_label.text = ''
        for button in self.buttons:
            button.text = ''

    def _reload_buttons(self):
        '''Used to set visible and reload selector'''
        for (button, name) in zip(self.buttons, self.names):
            if name is self.names[self.selector]:
                button.text = '< ' + name + ' >'
            else:
                button.text = name


    def set_selector(self):
        '''Loops the selector around'''
        if self.selector < 0:
            self.selector += len(self.names)
        elif self.selector > len(self.names) - 1:
            self.selector -= len(self.names)
        self._reload_buttons()

    def select(self):
        select = self.calls[self.selector]
        if hasattr(select, '__call__'): select()
        self.set_invisible()


    def on_key_press(self, symbol, modifiers):
        if self.visible:

            if symbol == key.ENTER:
                self.select()

            if symbol == key.DOWN:
                self.selector += 1
                self.set_selector()

            elif symbol == key.UP:
                self.selector -= 1
                self.set_selector()
