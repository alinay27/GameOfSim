import arcade
import math
screen_width = 800
screen_height = 800

def makeVertices():
    vertices = []
    for i in range(6):
        angle = math.pi / 3 * i
        x = 400 + 250 * math.cos(math.radians(angle * i))
        y = 400 + 250 * math.sin(math.radians(angle * i))

        vertices.append((x, y))
    return vertices

v1, v2, v3, v4, v5, v6 = makeVertices()

class SimGame(arcade.Window):
    def __init__(self):
        super().__init__(screen_width, screen_height, "Game of Sim")
        self.vertices = makeVertices()
        self.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        for x, y in self.vertices:
            arcade.draw_circle_filled(x, y, 10, arcade.color.BLACK)

self = SimGame()
running = True
while running:
    self.on_draw()
    arcade.finish_render()
    arcade.pause(0.01)
