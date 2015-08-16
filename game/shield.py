import pyglet
from pyglet.sprite import Sprite

from . import resources

class Shield:
    """Sprite controller for shield up animation"""
    def __init__(self, batch):

        _frames = resources.shield_images
        self._frames = [Sprite(img=frame, batch=batch) for frame in _frames]

        for frame in self._frames:
            frame.visible = False
            frame.scale = 1.5

        self._frame = 0
        
        self.frames_delta = 0.5
        self.counter = .0

        self.up = False
        self.frame = self._frames[0]

        self.x = 0
        self.y = 0


    def update(self, dt):        
        if True:
            self.counter += dt

            if self.counter >= self.frames_delta:
                self.counter = .0

                if self.up and self._frame < len(self._frames)-1:
                    self.frame.visible = False
                    self._frame += 1

                elif not self.up and self._frame >= 0:
                    self.frame.visible = False
                    self._frame -= 1
                else:
                    return None
                self.frame = self._frames[self._frame]
                self.frame.visible = True

        self.frame.x = self.x
        self.frame.y = self.y

