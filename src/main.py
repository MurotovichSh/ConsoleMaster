import arcade
from views.menu import MainView

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ConsoleMaster"


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,
                           SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
