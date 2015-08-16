import pyglet
from pyglet.sprite import Sprite

class Shield:
    """Object that activates to protect the player"""
    def __init__(self):
        super().__init__(img=shield_images[-1], *args, **kwargs)

        self.reacts_to_bullets = False
        self.score_dif = -20

        self.animation_frames = sheild_images

    def up(self, time):
        """Plays shield up animation by switching local invul_sprite to frame 
        sprite and making other frames inisible"""
        #self.invul_sprite.visible = False

        for enu, sprite in enumerate(shield_sprites):
            if enu:
                shield_sprites[enu-1] = False

                sprite.visible = True
                self.invul_sprite = sprite

            else:
                sprite.visible = True
                self.invul_sprite = sprite

    def down(self, time):
        # play animation frames
        # stop at the end of the list
        pass

    def update(self):
        # yeilds the up and down generators