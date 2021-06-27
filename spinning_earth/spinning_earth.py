import pygame

import numpy as np
import os
from math import pi, sin, cos

try:
  os.environ["DISPLAY"]
except:
  os.environ["SDL_VIDEODRIVER"] = "dummy"


clock = pygame.time.Clock()
FPS = 30

WIDTH = 1600
HEIGHT = 1600

R = 250
MAP_WIDTH = 100
MAP_HEIGHT = 32




with open('spinning_earth/earth.txt', 'r') as file:
  data = [file.read().replace('\n', '').replace('-', '*').replace(' ', '-').replace('.', '*')]

ascii_chars = []
for line in data:
  for char in line:
    ascii_chars.append(char)

inverted_ascii_chars = ascii_chars[::-1]

pygame.init()
my_font = pygame.font.SysFont('arial', 20)

class Projection:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.screen = pygame.display.set_mode((width, height))
    self.background = (10, 10, 60)
    pygame.display.set_caption('ASCII 3D EARTH')
    self.surfaces = {}

  def addSurface(self, name, surface):
    self.surfaces[name] = surface

  def display(self):
    self.screen.fill(self.background)
    for surface in self.surfaces.values():
      i=0
      for node in surface.nodes:
        self.text = inverted_ascii_chars[i]
        self.text_surface = my_font.render(self.text, False, (0,255,0))
        if node[1] > 0:
          self.screen.blit(self.text_surface, (WIDTH / 2 + int(node[0]), (HEIGHT / 2 + int(node[2]))))
        i += 1

  def rotateAll(self, theta):
    for surface in self.surfaces.values():
      center = surface.findCenter()
      c = np.cos(theta)
      s = np.sin(theta)
      matrix = np.array([
        [c, -s, 0, 0], 
        [s, c, 0, 0], 
        [0, 0, 1, 0], 
        [0, 0, 0, 1]
      ])
      surface.rotate(center, matrix)


class Object:
  def __init__(self):
    self.nodes = np.zeros((0, 4))

  def addNodes(self, node_array):
    ones_column = np.ones((len(node_array), 1))
    ones_added = np.hstack((node_array, ones_column))
    self.nodes = np.vstack((self.nodes, ones_added))

  def findCenter(self):
    mean = self.nodes.mean(axis=0)
    return mean

  def rotate(self, center, matrix):
    for i, node in enumerate(self.nodes):
      self.nodes[i] = center + np.matmul(matrix, node-center)


xyz = []

for i in range(MAP_HEIGHT +1):
  lat = (pi/MAP_HEIGHT) + i
  for j in range(MAP_WIDTH+1):
    lon = (2*pi/MAP_WIDTH) * j
    x = round(R * sin(lat) * cos(lon), 2)
    y = round(R * sin(lat) * sin(lon), 2)
    z = round(R * cos(lat), 2)
    xyz.append((x,y,z))

print(len(xyz))

spin = 0
running = True
while running:
  clock.tick(FPS)

  pv = Projection(WIDTH, HEIGHT)

  # cube = Object()
  # cube_nodes = ([(x, y, z) for x in (200, 600) for y in (200, 600) for z in (200, 600)])
  # cube.addNodes(np.array(cube_nodes))
  # pv.addSurface('cube', cube)

  globe = Object()
  globe_nodes = [i for i in xyz]
  globe.addNodes(np.array(globe_nodes))
  pv.addSurface('globe', globe)

  pv.rotateAll(spin)
  pv.display()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  pygame.display.update()
  spin += 0.005