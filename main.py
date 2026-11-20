import random
import arcade
import math

screen_width = 800
screen_height = 800


def makeVertices():
    vertices = []
    for i in range(6):
        angle = math.pi / 3 * i
        x = screen_width / 2 + 250 * math.cos(angle)
        y = screen_height / 2 + 250 * math.sin(angle)
        vertices.append((x, y))
    return vertices


class SimGame(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, "Game of Sim")
        self.vertices = makeVertices()
        self.background_color = arcade.color.WHITE
        self.red_edges = set()
        self.blue_edges = set()
        self.line_color1 = arcade.color.RED
        self.line_color2 = arcade.color.BLUE
        self.bot_mode = False
        self.game_over = False
        self.winner_message = ""
        self.turn = 1
        self.selected_dot = None
        self.winner_text = arcade.Text(
            "", screen_width / 2, 730, arcade.color.RED, 24, anchor_x="center"
        )
        self.turn_text = arcade.Text(
            "", screen_width / 2, 730, arcade.color.BLACK, 20, anchor_x="center"
        )
        self.bot_control = arcade.Text(
            "B: Bot", screen_width / 2 - 150, 50, arcade.color.BLACK, 16, anchor_x="center"
        )
        self.two_player_control = arcade.Text(
            "P: Two Players", screen_width / 2, 50, arcade.color.BLUE, 16,
            anchor_x="center", bold=True,
        )
        self.restart_control = arcade.Text(
            "R: Restart", screen_width / 2 + 150, 50, arcade.color.BLACK, 16, anchor_x="center"
        )

    def on_draw(self):
        self.clear()
        for i, j in self.red_edges:
            start = self.vertices[i]
            end = self.vertices[j]
            arcade.draw_line(*start, *end, self.line_color1, 3)
        for i, j in self.blue_edges:
            start = self.vertices[i]
            end = self.vertices[j]
            arcade.draw_line(*start, *end, self.line_color2, 3)
        for i, (x, y) in enumerate(self.vertices):
            dot_color = arcade.color.BLACK
            if i == self.selected_dot:
                dot_color = self.line_color1 if self.turn == 1 else self.line_color2
            arcade.draw_circle_filled(x, y, 12, dot_color)

        if self.game_over:
            if self.winner_text.text != self.winner_message:
                self.winner_text.text = self.winner_message
            self.winner_text.draw()
        else:
            if self.turn == 1:
                self.message = "Player 1 (RED)"
            elif self.bot_mode:
                self.message = "Bot (BLUE)"
            else:
                self.message = "Player 2 (BLUE)"
            if self.turn_text.text != self.message:
                self.turn_text.text = self.message
            self.turn_text.draw()

        self.bot_control.draw()
        self.two_player_control.draw()
        self.restart_control.draw()

    def makes_triangle(self, edge, edges):
        a, b = edge
        for c in range(6):
            if c != a and c != b:
                edge1 = tuple(sorted((a, c)))
                edge2 = tuple(sorted((b, c)))
                if edge1 in edges and edge2 in edges:
                    return True
        return False

    def bot_move(self):  # bot chooses a line randomly
        if self.game_over or self.turn != 2:
            return
        open_edges = []
        safe_edges = []

        for i in range(6):
            for j in range(i + 1, 6):
                edge = (i, j)
                if edge not in self.red_edges and edge not in self.blue_edges:
                    open_edges.append(edge)
                    if not self.makes_triangle(edge, self.blue_edges):
                        safe_edges.append(edge)
        if len(safe_edges) > 0:
            edge = random.choice(safe_edges)
        elif len(open_edges) > 0:
            edge = random.choice(open_edges)
        else:
            return
        self.blue_edges.add(edge)
        if self.makes_triangle(edge, self.blue_edges):
            self.game_over = True
            self.winner_message = "Bot Loses! Player 1 Wins!"
        else:
            self.turn = 1

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT or self.game_over:
            return
        clicked_dot = None
        for i, (vx, vy) in enumerate(self.vertices):
            if math.hypot(x - vx, y - vy) <= 12:
                clicked_dot = i
                break
        if clicked_dot is None:
            return

        if self.selected_dot is None:
            self.selected_dot = clicked_dot
            return
        if self.selected_dot == clicked_dot:
            self.selected_dot = None
            return
        edge = tuple(sorted((self.selected_dot, clicked_dot)))
        self.selected_dot = None

        if edge in self.red_edges or edge in self.blue_edges:
            return

        if self.turn == 1:
            self.red_edges.add(edge)
            if self.makes_triangle(edge, self.red_edges):
                self.game_over = True
                if self.bot_mode:
                    self.winner_message = "Player 1 Loses! Bot Wins!"
                else:
                    self.winner_message = "Player 1 Loses! Player 2 Wins!"
            else:
                self.turn = 2
                if self.bot_mode:
                    self.bot_move()
        elif not self.bot_mode:
            self.blue_edges.add(edge)
            if self.makes_triangle(edge, self.blue_edges):
                self.game_over = True
                self.winner_message = "Player 2 Loses! Player 1 Wins!"
            else:
                self.turn = 1

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.B, arcade.key.P):
            self.bot_mode = key == arcade.key.B
            self.bot_control.color = arcade.color.BLUE if self.bot_mode else arcade.color.BLACK
            self.two_player_control.color = arcade.color.BLACK if self.bot_mode else arcade.color.BLUE
            self.bot_control.bold = self.bot_mode
            self.two_player_control.bold = not self.bot_mode
            self.restart()
        elif key == arcade.key.R:
            self.restart()

    def restart(self):
        self.red_edges.clear()
        self.blue_edges.clear()
        self.turn = 1
        self.selected_dot = None
        self.game_over = False
        self.winner_message = ""

def main():
    window = SimGame()
    arcade.run()

if __name__ == "__main__":
    main()
