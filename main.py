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