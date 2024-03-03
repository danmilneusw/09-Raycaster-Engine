# fps.py
import pygame

pygame.font.init()

class FPS:
    def __init__(self, clock):
        self.clock = clock
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (255, 255, 255))
 
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (255, 255, 255))
        display.blit(self.text, (0, 0))
