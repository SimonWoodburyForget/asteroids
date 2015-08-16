import pyglet
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.graphics import OrderedGroup
from pyglet.window import key

from . import resources


class HudObjects:
    """Game stats that are displayed and updated while playing the game.

    This object does not understand any game mechanics else then the
    numbers it displays

    Has 4 main property's:
        - lives
        - score
        - top_score
        - spawn

    All property's are set by setting it to a number.
        example: hud_objects_instance.lives = 4

    The label object is returned on setting to update the object on the window,
        without requiring more then one line of code to update the value

    Screen size is set by pushing the class's handlers to the window.
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
        """
        Gets the lives sprite objects, places them on the screen axis
            and returns them.

        Sets lives to interger then generates the right amount of sprites.
            Then returns sprite object.
        """
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
        """
        Gets the score label object, places on screen axis and returns it.

        Sets the score with interger, generates the label text with it,
            then returns label object with get.
        """
        self._score_label.x = 10
        self._score_label.y = self.height - 25
        return self._score_label
    @score.setter
    def score(self, score):
        self._score = score
        text = self._score_text.format(self._score)
        self._score_label.text = text
        return self.score


    @property
    def top_score(self):
        """
        Gets the spawn label object, places on screen axis and returns it.

        Sets the top_score with interger, generates the label text with it,
            then returns label object with get.
        """
        text = self._top_score_text.format(self._top_score)
        self._top_score_label.text = text
        self._top_score_label.x = 10
        self._top_score_label.y = self.height - 50
        return self._top_score_label
    @top_score.setter
    def top_score(self, top_score):
        self._top_score = top_score
        text = self._top_score_text.format(self._top_score)
        self._top_score_label.text = text
        return self.top_score


    @property
    def spawn(self):
        """
        Gets the spawn label object, places on screen axis and returns it.

        Sets the spawn with interger, generates label text with it,
            then returns label object with get
        """
        self._spawn_label.x = self.width / 2
        self._spawn_label.y = self.height - 25
        return self._spawn_label
    @spawn.setter
    def spawn(self, spawn):
        self._spawn = spawn
        text = self._spawn_text.format(self._spawn)
        self._spawn_label.text = text
        return self.spawn



    """
    Keeps both width and height always in sync with the screen_size
    """
    @property
    def width(self):
        """
        Gets the x axis of the screen object

        Sets the x axis of the screen object
        """
        return self.screen_size[0]
    @width.setter
    def width(self, value):
        self.screen_size = (value, self.width)

    @property
    def height(self):
        """
        Gets the y axis of the screen object

        Sets the y axis of the screen object
        """
        return self.screen_size[1]
    @height.setter
    def height(self):
        self.screen_size = (self.width, value)


    """event handled by pushing it to the window"""
    def on_resize(self, width, height):
        self.screen_size = (width, height)
        self.score
        self.top_score
        self.spawn
        self.lives



class Selection(Sprite):
    """
    Basic class to create menus with buttons that can let the user call
        other game functionality.
    """
    def __init__(self, name, screen_size, *args, **kwargs):
        super().__init__(img=resources.menu_background, group=OrderedGroup(0),
                         *args, **kwargs)
        # sprite needed attributes
        self.img = resources.menu_background
        self.x = screen_size[0]/2
        self.y = screen_size[1]/2
        self.visible = False

        self.name = name
        self.name_label = Label(
            anchor_x='center',
            batch=self.batch,
            group=OrderedGroup(1)
        )
        self._position_name

        # items to be called when set visible
        self._auto_calls = []

        # holds button related stuff
        self.names = []
        self.buttons = []
        self.calls = []

        # position of selected item
        self.selector = 0

    def auto_call(self, *calls):
        """Any number of callable objects can be sent, they will be
            added to the automatically called objects list when set visible.

        Originally made to save the game on game_over and menu open"""
        for call in calls:
            self._auto_calls.append(call)

    def insert(self, name, call):
        """Used to call inset button name and callable object in list
            buttons will be displaed in order inserted"""
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
        """Sets background and buttons visible
            calls objects that need to be called automatically"""
        if not self.visible: # game window seems to call this on repeat,
                             # temporary fix to avoid saving score over it self.

            for call in self._auto_calls:
                call()
            self.visible = True
            self.name_label.text = self.name
            self._reload_buttons()

    def set_invisible(self):
        """Sets background and buttons invisible and resets selector"""
        self.visible = False
        self.selector = 0
        self.name_label.text = ''
        for button in self.buttons:
            button.text = ''


    def set_selector(self):
        """Used to move selector up or down"""

        # check if selector is out of range and loops it around.
        if self.selector < 0:
            self.selector += len(self.names)
        elif self.selector > len(self.names) - 1:
            self.selector -= len(self.names)

        self._reload_buttons()

    def select(self):
        """Used to call object on selection"""
        select = self.calls[self.selector]
        if hasattr(select, '__call__'): select()
        self.set_invisible()

    def _reload_buttons(self):
        """Reloads the state of the buttons,
            Used to update the selector"""

        for (button, name) in zip(self.buttons, self.names):
            if name is self.names[self.selector]:
                button.text = '< ' + name + ' >'
            else:
                button.text = name



    def _position_name(self):
        """Position title name
            based on current menu state"""
        self.name_label.x = self.x
        self.name_label.y = self.y + self.image.height/2 - 30

    def _position_buttons(self):
        """Position indefinite number of buttons
            based on the current menu state"""
        _x = self.x
        _y = self.y + self.image.height/2 - 70
        for count, button in enumerate(self.buttons):
            button.x = _x
            button.y = _y - count * 20



    """events handled by pushing them to the window object"""
    def on_resize(self, width, height):
        self.x = width/2
        self.y = height/2

        self._position_name()
        self._position_buttons()


    def on_key_press(self, symbol, modifiers):
        """Handles moving the selector from button to button
            and calling objects when selected"""

        if self.visible:

            if symbol == key.ENTER:
                self.select()

            if symbol == key.DOWN:
                self.selector += 1
                self.set_selector()

            elif symbol == key.UP:
                self.selector -= 1
                self.set_selector()
