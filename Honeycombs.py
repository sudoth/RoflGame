import pygame
import random
import math

SQRT3 = math.sqrt(3)
SIN = SQRT3 / 2
ORANGE = (247, 187, 57)
YELLOW = (250, 230, 115)
BACKGROUND = (235, 185, 105)
EDGE = (180, 115, 63)
WIDTH = 700
HEIGHT = 700
DISTANCE = 10
DELAY = 300

class Honeycomb:

  def init(self):
    pygame.init()
    screen_info = pygame.display.Info()
    self.width, self.height = WIDTH, HEIGHT
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

  def CreateHoneycombs(self):
    self.screen.fill(BACKGROUND)
    x_0 = WIDTH // 2
    y_0 = HEIGHT // 2
    honeycombs = []
    honeycombs.append(Polygon(x_0, y_0, EDGE))
    dist = DISTANCE + 2 * honeycombs[0].side_size * SIN
    honeycombs.append(Polygon(x_0 - SIN * dist, y_0 - 1 / 2 * dist, EDGE))
    honeycombs.append(Polygon(x_0, y_0 - dist, EDGE))
    honeycombs.append(Polygon(x_0 + SIN * dist, y_0 - 1 / 2 * dist, EDGE))
    honeycombs.append(Polygon(x_0 + SIN * dist, y_0 + 1 / 2 * dist, EDGE))
    honeycombs.append(Polygon(x_0, y_0 + dist, EDGE))
    honeycombs.append(Polygon(x_0 - SIN * dist, y_0 + 1 / 2 * dist, EDGE))
    self.DrawHoneycombs(honeycombs)
    return honeycombs

  def DrawHoneycombs(self, honeycombs):
    for i in range(len(honeycombs)):
      honeycombs[i].Draw(self.screen)
      new_polygon = Polygon(honeycombs[i].x, honeycombs[i].y, ORANGE, 82)
      new_polygon.Draw(self.screen)
    pygame.display.update()

  def ShowSequence(self, sequence, honeycombs):
    pygame.event.pump()
    for i in sequence:
      new_polygon = Polygon(honeycombs[i].x, honeycombs[i].y, YELLOW, 80)
      new_polygon.Draw(self.screen)
      pygame.display.flip()
      pygame.event.pump()
      pygame.time.delay(DELAY)
      self.DrawHoneycombs(honeycombs)
      pygame.event.pump()
      pygame.time.delay(DELAY)

  def Run(self):
    game_over = False
    snd1 = pygame.mixer.Sound("snd1.wav")
    snd2 = pygame.mixer.Sound("snd2.wav")
    snd3 = pygame.mixer.Sound("snd3.wav")
    honeycombs = self.CreateHoneycombs()
    sequence = [random.randint(0, 6)]
    queue = [sequence[0]]
    self.ShowSequence(sequence, honeycombs)
    print(sequence)

    while not game_over:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          game_over = False
          pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          x, y = pygame.mouse.get_pos()
          if not honeycombs[queue[-1]].Popal(x, y):
            print("kal")
            pygame.mixer.Sound.play(snd3)
            pygame.event.pump()
            pygame.time.delay(4 * DELAY)
            game_over = True
            #смэрть
          else:
            pygame.mixer.Sound.play(snd1)
            queue.pop()
            if len(queue) == 0:
              sequence.append(random.randint(0, 6))
              self.ShowSequence(sequence, honeycombs)
              queue = sequence.copy()
              queue.reverse()
              print(sequence)

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Vector:
  def __init__(self, point_a : Point, point_b : Point):
    self.x = point_b.x - point_a.x
    self.y = point_b.y - point_a.y

def VectorProduct(a : Vector, b : Vector):
  return a.x * b.y - a.y * b.x

class Polygon:
  def __init__(self, x, y, color, side_size = 100):
    self.x = x
    self.y = y
    self.color = color
    self.clicked = False
    self.side_size = side_size

  def PolygonPoint(self, number):
    if (number == 0):
      return Point(-self.side_size / 2 + self.x, SQRT3 * self.side_size / 2 + self.y)
    if (number == 1):
      return Point(self.side_size / 2 + self.x, SQRT3 * self.side_size / 2 + self.y)
    if (number == 2):
      return Point(self.side_size + self.x, self.y)      
    if (number == 3):
      return Point(self.side_size / 2 + self.x, -SQRT3 * self.side_size / 2 + self.y)     
    if (number == 4):
      return Point(-self.side_size / 2 + self.x, -SQRT3 * self.side_size / 2 + self.y)
    if (number == 5):
      return Point(-self.side_size + self.x, self.y)
    
  def Draw(self, screen):
    coordinades = []
    for i in range(6):
      point = self.PolygonPoint(i)
      coordinades.append((point.x, point.y))
    pygame.draw.polygon(screen, self.color, coordinades)


  def Popal(self, x, y):
    for i in range(6):
      a = self.PolygonPoint(i)
      b = self.PolygonPoint((i + 1) % 6)
      c = Point(x, y)
      if VectorProduct(Vector(a, b), Vector(a, c)) > 0:
        return False
    return True

visual_memory_honeycombs_test = Honeycomb()
visual_memory_honeycombs_test.init()
visual_memory_honeycombs_test.Run()
