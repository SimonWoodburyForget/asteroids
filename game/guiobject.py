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

        self._score_label = Label(batch=self.batch)
        self._score_text = 'Score: {}'
        self._score = 0

        self._spawn_label = Label(batch=self.batch)
        self._spawn_label.anchor_x = 'center'
        self._spawn_text = 'Spawn: {}'
        self._spawn = 0

    @property
    def score(self):
        '''To always returns the right label for it's local screen size'''
        text = self._score_text.format(self._score)
        self._score_label.text = text
        self._score_label.x = 10
        self._score_label.y = self.height - 25
        return self._score_label

    @score.setter
    def score(self, score):
        '''Setting score locally has an int'''
        self._score = score
        return self.score

    @property
    def spawn(self):
        '''To always returns the right label for it's local screen size'''
        text = self._spawn_text.format(self._spawn)
        self._spawn_label.text = text
        self._spawn_label.x = self.width / 2
        self._spawn_label.y = self.height - 25
        return self._spawn_label

    @spawn.setter
    def spawn(self, spawn):
        '''Setting spawn locally has an int'''
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


class Selection(Sprite):
    """Basic class to create menu, with buttons, and functions when pressed"""
    def __init__(self, name, *args, **kwargs):
        super().__init__(img=menu_background,
            group=OrderedGroup(0), *args, **kwargs)
        self.name = name
        self.visible = False

        self.names = []
        self.buttons = []
        self.calls = []
        self.selector = 0

        self.name_label = Label(
            x=self.x,
            y=self.y + self.image.height/2 - 30,
            anchor_x='center',
            batch=self.batch,
            group=OrderedGroup(1)
        )


    def insert(self, name, call):
        button = Label(
            x=self.x,
            y=(self.y + self.image.height/2 - 70
                - (len(self.names) * 20)),
            anchor_x='center',
            batch=self.batch,
            group=OrderedGroup(1)
        )
        self.names.append(name)
        self.buttons.append(button)
        self.calls.append(call)


    def set_visible(self):
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
