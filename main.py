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
            arcade.draw_circle_filled(x, y, 12, arcade.color.BLACK)

        if self.game_over:
            arcade.draw_text(self.winner_message, screen_width/2, 730, arcade.color.RED, 24, anchor_x = "center")
        else:
            if self.turn == 1:
                message = "Player 1 (RED)"
            else:
                message = "Player 2 (BLUE)"
            arcade.draw_text(message, screen_width/2, 730, arcade.color.BLACK, 20, anchor_x= "center")
        arcade.draw_text("Click two dots to draw a line", screen_width/2, 50, arcade.color.BLACK, 16, anchor_x="center")

    def makes_triangle(self, edge, edges):
        a, b = edge
        for c in range(6):
            if c != a and c != b:
                edge1 = tuple(sorted(a,c))
                edge2 = tuple(sorted(b,c))
                if edge1 in edges and edge2 in edges:
                    return True
        return False
    def on_update(self, delta_time):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT or self.game_over:
            return
        clicked_dot = None
        for i, (vx, vy) in enumerate(self.vertices):
            if math.hypot(x-vx, y-vy) <= 12:
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
                self.winner_message = "Player 1 Loses! Player 2 Wins!"
            else:
                self.turn = 2
        else:
            self.blue_edges.add(edge)
            if self.makes_triangle(edge, self.blue_edges):
                self.game_over = True
                self.winner_message = "Player 1 Loses! Player 2 Wins!"
            else:
                self.turn = 1
        
def main():
    window = SimGame()
    arcade.run()
if __name__ == "__main__":
    main()

