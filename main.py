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

    def on_draw(self):
        self.clear()
        for i, start in enumerate(self.vertices):
            for end in self.vertices[i + 1:]:
                arcade.draw_line(*start, *end, arcade.color.GRAY, 2)
        for x, y in self.vertices:
            arcade.draw_circle_filled(x, y, 10, arcade.color.BLACK)

def main():
    window = SimGame()
    arcade.run()
if __name__ == "__main__":
    main()

