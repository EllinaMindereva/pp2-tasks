import pygame
import math
import datetime

class TheClock:
    def __init__(self, center, size):
        self.size = size
        self.center = center
    
    def update(self):
        pass 

    def get_angle(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second 

        min_angle = math.radians((minutes + seconds / 60) * 6 - 90)
        sec_angle = math.radians(seconds * 6 - 90)

        return min_angle, sec_angle

    def draw_hand(self, screen, angle, length, width, color):
        x = self.center[0] + length * math.cos(angle)
        y = self.center[1] + length * math.sin(angle)
        pygame.draw.line(screen, color, self.center, (x, y), width)

    def draw(self, screen):
        min_angle, sec_angle = self.get_angle()

        self.draw_hand(screen, min_angle, 200, 12, (0, 0, 0))
        self.draw_hand(screen, sec_angle, 250, 5, (0, 0, 255))

        pygame.draw.circle(screen, (0, 0, 0), self.center, 15)
