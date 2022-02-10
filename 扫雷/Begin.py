from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import game


Builder.load_file('Begin.kv')


class BeginWin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def easy_game(self):
        game.Create_num_mine(13)
        self.parent.parent.current = 'scrn_game'

    def normal_game(self):
        game.Create_num_mine(16)
        self.parent.parent.current = 'scrn_game'

    def hard_game(self):
        game.Create_num_mine(20)
        self.parent.parent.current = 'scrn_game'


