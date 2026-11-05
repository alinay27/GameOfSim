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
        #Dots cover the endpoints, so only clicks on visible lines count
        for vx, vy in self.vertices:
            if math.hypot(x-vx, y-vy) <= 12:
                return

        closest_edge = None
        closest_distance = 15

        for i in range(6):
            for j in range(i+1, 6):
                if (i, j) in self.red_edges:
                    continue
                if (i, j) in self.blue_edges:
                    continue
                x1, y1 = self.vertices[i]
                x2, y2 = self.vertices[j]
                dx = x2 - x1
                dy = y2 - y1

                click = ((x - x1) * dx + (y-y1) * dy) / (dx*dx + dy*dy)
                closest_x = x1 + click * dx
                closest_y = y1 + click * dy
                distance = math.hypot(x - closest_x, y - closest_y)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_edge = (i, j)
                
        if closest_edge is not None:
            if self.turn == 1:
                self.red_edges.add(closest_edge)
                if self.makes_triangle(closest_edge, self.red_edges):
                    self.game_over = True
                    self.winner_message = "Player 1 Loses! Player 2 Wins!"
                self.turn = 2

                if self.bot_mode and not self.game_over:
                    self.bot_move()
                else:
                    self.turn = 2

            elif not self.bot_mode:
                self.blue_edges.add(closest_edge)
                if self.makes_triangle(closest_edge, self.blue_edges):
                    self.game_over = True
                    self.winner_message = "Player 2 Loses! Player 1 Wins!"
                self.turn = 1
        
def main():
    window = SimGame()
    arcade.run()
if __name__ == "__main__":
    main()

