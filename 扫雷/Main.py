from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from Begin import BeginWin
from game import GameWin


class MainWin(BoxLayout):
    Begin_widget = BeginWin()
    Game_widget = GameWin()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_beg.add_widget(self.Begin_widget)
        self.ids.scrn_game.add_widget(self.Game_widget)


class MainApp(App):
    def build(self):
        return MainWin()


if __name__ == '__main__':
    sa = MainApp()
    sa.run()