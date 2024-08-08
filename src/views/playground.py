import arcade
import arcade.gui
import subprocess
import random
import math
import importlib

menu = importlib.import_module('.menu', package='views')
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Terminal Playground"
MUSIC_FILE = "music/warm-happy-rap.wav"


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
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]

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

class TerminalView(arcade.View):
    def __init__(self, menu_view):
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
        self.music = arcade.load_sound(MUSIC_FILE)
        self.music_player = self.music.play(loop=False)
        self.music_player.pause()

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

        back_button = arcade.gui.UIFlatButton(text="Back", width=200, height=50, style=style)
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            child=back_button
        )
        self.manager.add(anchor)

        @back_button.event("on_click")
        def on_click_back_button(event):
            menu_view = menu.MenuView(self)
            self.window.show_view(menu_view)

    def on_draw(self):
        arcade.start_render()
        # Backround animation
        self.background_animation.on_draw()

        y = SCREEN_HEIGHT - 50 + self.scroll_offset
        for line in self.terminal_output:
            if 20 <= y <= SCREEN_HEIGHT - 30:
                arcade.draw_text(line, 10, y, arcade.color.WHITE, 12, width=SCREEN_WIDTH - 20, align="left", anchor_x="left", anchor_y="top", font_name="Courier", multiline=True)
            y -= 20

        # Glowing effect
        if self.glowing_effect:
            self.glowing_effect.on_draw()

        # Command line at fixed position
        arcade.draw_text(">> " + self.command_buffer, 10, 20, arcade.color.GREEN, 12, width=SCREEN_WIDTH - 20, align="left", anchor_x="left", anchor_y="top", font_name="Courier")

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
        max_scroll = max(0, len(self.terminal_output) * 20 - (SCREEN_HEIGHT - 50))
        min_scroll = min(0, SCREEN_HEIGHT - 50 - len(self.terminal_output) * 20)
        self.target_scroll_offset = min(max_scroll, self.target_scroll_offset)
        self.target_scroll_offset = max(min_scroll, self.target_scroll_offset)

    def execute_command(self):
        command = self.command_buffer.strip()
        self.terminal_output.append(">> " + command)
        self.glowing_effect = GlowingEffect(">> ", 10, 20, arcade.color.GREEN, 12, "Courier")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                stdout_lines = result.stdout.split('\n')
                wrapped_lines = self.wrap_lines(stdout_lines)
                self.terminal_output.extend(wrapped_lines)
                self.start_typing_animation(wrapped_lines)
            if result.stderr:
                stderr_lines = result.stderr.split('\n')
                wrapped_lines = self.wrap_lines(stderr_lines)
                self.terminal_output.extend(wrapped_lines)
                self.start_typing_animation(wrapped_lines)
        except Exception as e:
            self.terminal_output.append("Error: " + str(e))

        # Automatic scrolldown
        self.target_scroll_offset = max(0, len(self.terminal_output) * 20 - (SCREEN_HEIGHT - 50))

        self.command_buffer = ""

    def wrap_lines(self, lines):
        wrapped_lines = []
        for line in lines:
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + word + ' '
                text = arcade.Text(test_line, 0, 0, font_name="Courier", font_size=12)
                if text.width > SCREEN_WIDTH - 20:
                    wrapped_lines.append(current_line)
                    current_line = word + ' '
                else:
                    current_line = test_line
            wrapped_lines.append(current_line.strip())
        return wrapped_lines

    def start_typing_animation(self, text_lines):
        y = SCREEN_HEIGHT - 50 - 20 * len(self.terminal_output)
        self.typing_animation = TypingAnimation("\n".join(text_lines), 10, y, arcade.color.WHITE, 12, "Courier")

    def on_update(self, delta_time):
        self.background_animation.on_update(delta_time)

        if self.typing_animation:
            self.typing_animation.on_update(delta_time)
            if self.typing_animation.finished:
                self.typing_animation = None

        if self.glowing_effect:
            self.glowing_effect.on_update(delta_time)

        # Smooth scrolling
        scroll_diff = self.target_scroll_offset - self.scroll_offset
        self.scroll_offset += scroll_diff * 0.5

    def start_music(self):
        if not self.music_player:
            self.music_player = self.music.play(loop=False)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    terminal_view = TerminalView(menu.MenuView(None))
    window.show_view(terminal_view)
    arcade.run()

if __name__ == "__main__":
    main()
