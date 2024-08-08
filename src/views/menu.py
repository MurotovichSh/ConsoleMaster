import arcade
import arcade.gui
import importlib
from commands import *
from exercises import *
import math
import random
TerminalView = importlib.import_module('.playground', package='views')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Menu"

# Music file path
MUSIC_FILE = "music/warm-happy-rap.wav"
# Background image
IMAGE_FILE = "images/main_background.png"


class MainView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture(IMAGE_FILE)

        # Load and play music
        self.music = arcade.load_sound(MUSIC_FILE)
        self.music_player = self.music.play(loop=True)

        # Custom button style
        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        switch_menu_button = arcade.gui.UIFlatButton(
            text="Start game", width=200, style=style)

        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        # Anchor to position the button on the screen
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=switch_menu_button
        )

        self.manager.add(anchor)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color((35, 39, 42))
        self.manager.enable()
        # Resume the music when showing the view
        self.music_player.play()

    def on_draw(self):
        """ Render the screen """
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        self.manager.draw()


class DetailedInfoView(arcade.View):
    def __init__(self, commands, exercises, game_view, menu_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.commands = commands
        self.exercises = exercises
        self.game_view = game_view

        # Custom button style
        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        exercises_button = arcade.gui.UIFlatButton(
            text="Start Exercises", width=200, style=style)

        back_button = arcade.gui.UIFlatButton(
            text="Back", width=200, style=style)

        @exercises_button.event("on_click")
        def on_click_exercises_button(event):
            terminal_view = ExerciseTerminalView(self.exercises)
            self.window.show_view(terminal_view)

        @back_button.event("on_click")
        def on_click_back_button(event):
            self.window.show_view(self.menu_view)

        # Create a vertical box layout for buttons and command info
        v_box = arcade.gui.UIBoxLayout()

        for command in self.commands:
            command_text = f"{command['name']}: {command['description']}"
            command_label = arcade.gui.UILabel(
                text=command_text, width=700, height=50, font_size=18,
                font_name="calibri", style=style
            )
            v_box.add(command_label.with_space_around(bottom=20))

        v_box.add(exercises_button.with_space_around(top=20))
        v_box.add(back_button.with_space_around(top=20))

        # Anchor the vertical box layout in the center of the screen
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=v_box
        )

        self.manager.add(anchor)
        self.menu_view = menu_view

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color((28, 31, 34))
        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


class MusicView(arcade.View):
    def __init__(self, menu_view, main_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture(IMAGE_FILE)
        self.menu_view = menu_view
        self.main_view = main_view

        # Custom button style
        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        stop_music_button = arcade.gui.UIFlatButton(
            text="Stop music", width=300, style=style
        )
        start_music_button = arcade.gui.UIFlatButton(
            text="Start music", width=300, style=style
        )
        back_button = arcade.gui.UIFlatButton(
            text="Back", width=200, style=style
        )

        v_box = arcade.gui.UIBoxLayout()
        v_box.add(stop_music_button.with_space_around(bottom=20))
        v_box.add(start_music_button.with_space_around(bottom=20))
        v_box.add(back_button.with_space_around(bottom=20))

        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=v_box
        )
        self.manager.add(anchor)

        @stop_music_button.event("on_click")
        def on_click_stop_music_button(event):
            self.main_view.music_player.pause()

        @start_music_button.event("on_click")
        def on_click_start_music_button(event):
            self.main_view.music_player.play()

        @back_button.event("on_click")
        def on_click_back_button(event):
            self.window.show_view(self.menu_view)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color((28, 31, 34))
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        self.manager.draw()


class GameView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture(IMAGE_FILE)

        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        easy_button = arcade.gui.UIFlatButton(
            text="Easy", width=300, style=style
        )
        medium_button = arcade.gui.UIFlatButton(
            text="Medium", width=300, style=style
        )
        hard_button = arcade.gui.UIFlatButton(
            text="Hard", width=300, style=style
        )
        back_button = arcade.gui.UIFlatButton(
            text="Back", width=300, style=style
        )

        # Create a vertical box layout for buttons
        v_box = arcade.gui.UIBoxLayout()

        # Add buttons to the vertical box layout
        v_box.add(easy_button.with_space_around(bottom=20))
        v_box.add(medium_button.with_space_around(bottom=20))
        v_box.add(hard_button.with_space_around(bottom=20))
        v_box.add(back_button.with_space_around(top=20))

        # Anchor the vertical box layout in the center of the screen
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=v_box
        )

        self.manager.add(anchor)
        self.menu_view = menu_view

        @easy_button.event("on_click")
        def on_click_easy_button(event):
            detailed_view = DetailedInfoView(
                easy_commands, easy_exercises, menu_view, self
            )
            self.window.show_view(detailed_view)

        @medium_button.event("on_click")
        def on_click_medium_button(event):
            detailed_view = DetailedInfoView(
                medium_commands, medium_exercises, menu_view, self
            )
            self.window.show_view(detailed_view)

        @hard_button.event("on_click")
        def on_click_hard_button(event):
            detailed_view = DetailedInfoView(
                hard_commands, hard_exercises, menu_view, self
            )
            self.window.show_view(detailed_view)

        @back_button.event("on_click")
        def on_click_back_button(event):
            self.window.show_view(self.menu_view)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color((28, 31, 34))
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        self.manager.draw()


class MenuView(arcade.View):
    def __init__(self, main_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.background = arcade.load_texture(IMAGE_FILE)
        self.main_view = main_view

        # Custom button style
        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        game_button = arcade.gui.UIFlatButton(
            text="Start", width=300, style=style
        )
        music_button = arcade.gui.UIFlatButton(
            text="Music", width=300, style=style
        )
        terminal_button = arcade.gui.UIFlatButton(
            text="Terminal Playground", width=300, style=style
        )
        exit_button = arcade.gui.UIFlatButton(
            text="Exit", width=300, style=style
        )

        v_box = arcade.gui.UIBoxLayout()

        # Add buttons to the vertical box layout
        v_box.add(game_button.with_space_around(bottom=20))
        v_box.add(music_button.with_space_around(bottom=20))
        v_box.add(terminal_button.with_space_around(bottom=20))
        v_box.add(exit_button.with_space_around(top=20))

        # Anchor the vertical box layout in the center of the screen
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="center_x",
            anchor_y="center_y",
            child=v_box
        )

        self.manager.add(anchor)

        @terminal_button.event("on_click")
        def on_click_terminal_button(event):
            terminal_view = TerminalView.TerminalView(self.main_view)
            self.window.show_view(terminal_view)

        @game_button.event("on_click")
        def on_click_game_button(event):
            game_view = GameView(self)
            self.window.show_view(game_view)

        @exit_button.event("on_click")
        def on_click_exit_button(event):
            arcade.exit()

        @music_button.event("on_click")
        def on_click_music_button(event):
            music_view = MusicView(self, self.main_view)
            self.window.show_view(music_view)

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        arcade.set_background_color((35, 39, 42))
        self.manager.enable()

    def on_draw(self):
        self.clear()
        # Draw the background image first
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.window.width, self.window.height, self.background
        )
        self.manager.draw()


class TypingAnimation:
    def __init__(self, text, x, y, color, font_size=12, font_name="Courier"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.font_name = font_name
        self.typing_index = 0
        self.finished = False

    def on_update(self, delta_time):
        if self.typing_index < len(self.text):
            self.typing_index += 1
        else:
            self.finished = True

    def on_draw(self):
        arcade.draw_text(
            self.text[:self.typing_index],
            self.x,
            self.y,
            self.color,
            self.font_size,
            width=SCREEN_WIDTH - 20,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="top",
            multiline=True
        )


class GlowingEffect:
    def __init__(self, text, x, y, color, font_size=12, font_name="Courier"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = font_size
        self.font_name = font_name
        self.glow_phase = 0

    def on_update(self, delta_time):
        self.glow_phase += delta_time * 5
        if self.glow_phase > 1:
            self.glow_phase = 0

    def on_draw(self):
        alpha = int((0.5 + 0.5 * math.sin(self.glow_phase * math.pi)) * 255)
        color = (*self.color[:3], alpha)
        arcade.draw_text(
            self.text,
            self.x,
            self.y,
            color,
            self.font_size,
            font_name=self.font_name,
            anchor_x="left",
            anchor_y="top"
        )


class BackgroundAnimation:
    def __init__(self):
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(
            0, SCREEN_HEIGHT)) for _ in range(100)]

    def on_update(self, delta_time):
        for i, (x, y) in enumerate(self.stars):
            y -= 1
            if y < 0:
                y = SCREEN_HEIGHT
                x = random.randint(0, SCREEN_WIDTH)
            self.stars[i] = (x, y)

    def on_draw(self):
        for x, y in self.stars:
            arcade.draw_point(x, y, arcade.color.WHITE, 2)


class ExerciseTerminalView(arcade.View):
    def __init__(self, exercises=None):
        super().__init__()
        self.command_buffer = ""
        self.terminal_output = []
        self.scroll_offset = 0
        self.target_scroll_offset = 0
        self.typing_animation = None
        self.glowing_effect = None
        self.background_animation = BackgroundAnimation()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.exercises = exercises or []
        self.current_exercise_index = 0

        # Custom button style
        style = {
            "font_name": ("calibri", "arial"),
            "font_size": 18,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": (50, 130, 184),
            "bg_color": arcade.color.PURPLE,
            "bg_color_pressed": arcade.color.PURPLE,
            "bg_color_hover": arcade.color.PURPLE,
        }

        back_button = arcade.gui.UIFlatButton(
            text="Back", width=200, height=50, style=style)
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            child=back_button
        )
        self.manager.add(anchor)

        @back_button.event("on_click")
        def on_click_back_button(event):
            menu_view = MenuView(self)
            self.window.show_view(menu_view)

        if self.exercises:
            self.show_exercise()

    def show_exercise(self):
        if self.current_exercise_index < len(self.exercises):
            question = self.exercises[self.current_exercise_index]['question']
            self.terminal_output.append(f"Exercise: {question}")
        else:
            self.terminal_output.append("No more exercises available.")

    def on_draw(self):
        arcade.start_render()
        self.background_animation.on_draw()

        y = SCREEN_HEIGHT - 50 + self.scroll_offset
        for entry in self.terminal_output:
            if isinstance(entry, dict):
                line = entry['text']
                color = entry['color']
            else:
                line = entry
                color = arcade.color.WHITE

            if 20 <= y <= SCREEN_HEIGHT - 30:
                arcade.draw_text(line, 10, y, color, 12, width=SCREEN_WIDTH - 20, align="left",
                                 anchor_x="left", anchor_y="top", font_name="Courier", multiline=True)
            y -= 20

        if self.glowing_effect:
            self.glowing_effect.on_draw()

        arcade.draw_text(">> " + self.command_buffer, 10, 20, arcade.color.WHITE, 12,
                         width=SCREEN_WIDTH - 20, align="left", anchor_x="left", anchor_y="top", font_name="Courier")

        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.execute_command()
        elif key == arcade.key.BACKSPACE:
            self.command_buffer = self.command_buffer[:-1]
        elif key == arcade.key.ESCAPE:
            self.command_buffer = ""
        else:
            self.command_buffer += chr(key)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.target_scroll_offset += scroll_y * 20
        max_scroll = max(0, len(self.terminal_output)
                         * 20 - (SCREEN_HEIGHT - 50))
        min_scroll = min(0, SCREEN_HEIGHT - 50 -
                         len(self.terminal_output) * 20)
        self.target_scroll_offset = min(max_scroll, self.target_scroll_offset)
        self.target_scroll_offset = max(min_scroll, self.target_scroll_offset)

    def execute_command(self):
        command = self.command_buffer.strip()
        self.terminal_output.append(">> " + command)
        self.glowing_effect = GlowingEffect(
            ">> ", 10, 20, arcade.color.GREEN, 12, "Courier")

        if self.current_exercise_index < len(self.exercises):
            correct_answer = self.exercises[self.current_exercise_index]['answer']
            if command == correct_answer:
                self.terminal_output.append(
                    {"text": "Great! You got it right.", "color": arcade.color.GREEN})
                self.start_typing_animation(["Great! You got it right."])
                self.current_exercise_index += 1
                self.show_exercise()
            else:
                self.terminal_output.append(
                    {"text": "Incorrect. Try again.", "color": arcade.color.RED})
                self.start_typing_animation(["Incorrect. Try again."])
        else:
            self.terminal_output.append("Time to move on to the next level!")

        self.command_buffer = ""

    def wrap_lines(self, lines):
        wrapped_lines = []
        for line in lines:
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + word + ' '
                text = arcade.Text(
                    test_line, 0, 0, font_name="Courier", font_size=12)
                if text.width > SCREEN_WIDTH - 20:
                    wrapped_lines.append(current_line)
                    current_line = word + ' '
                else:
                    current_line = test_line
            wrapped_lines.append(current_line.strip())
        return wrapped_lines

    def start_typing_animation(self, text_lines):
        y = SCREEN_HEIGHT - 50 - 20 * len(self.terminal_output)
        self.typing_animation = TypingAnimation(
            "\n".join(text_lines), 10, y, arcade.color.WHITE, 12, "Courier")

    def on_update(self, delta_time):
        self.background_animation.on_update(delta_time)

        if self.typing_animation:
            self.typing_animation.on_update(delta_time)
            if self.typing_animation.finished:
                self.typing_animation = None

        if self.glowing_effect:
            self.glowing_effect.on_update(delta_time)

        scroll_diff = self.target_scroll_offset - self.scroll_offset
        self.scroll_offset += scroll_diff * 0.5


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,
                           SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()
