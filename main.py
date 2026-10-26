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
        self.clicked_edge = None
        self.red_edges = set()
        self.line_color1 = arcade.color.RED
        self.line_color2 = arcade.color.BLUE

    def on_draw(self):
        self.clear()
        for i, start in enumerate(self.vertices):
            for j in range(i + 1, len(self.vertices)):
                end = self.vertices[j]
                color = self.line_color1 if (i, j) in self.red_edges else arcade.color.WHITE
                arcade.draw_line(*start, *end, color, 2)
        for x, y in self.vertices:
            arcade.draw_circle_filled(x, y, 12, arcade.color.BLACK)
    def on_update(self, delta_time):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        # Dots cover the endpoints, so only clicks on visible lines count.
        if any(math.hypot(x - vx, y - vy) <= 12 for vx, vy in self.vertices):
            return

        closest_edge = None
        closest_distance = 8
        

def main():
    window = SimGame()
    arcade.run()
if __name__ == "__main__":
    main()

