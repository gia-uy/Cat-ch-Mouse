import pygame
from define import *

class Player():
    x = 0
    y = 0
    color = ""
    def __init__(self, color,x, y, image) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.image = image
    def show(self, surface):
       surface.blit(self.image, (self.x, self.y))
    def move_up(self):
        self.y -= PLAYER_VANTOC
        if self.y <  0:
            self.y = 0
        
    def move_down(self):
        self.y += PLAYER_VANTOC
        if self.y > CHIEUCAO - PLAYER_CAO :
            self.y = CHIEUCAO - PLAYER_CAO