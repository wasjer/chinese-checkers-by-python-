import pygame
from pygame.sprite import Sprite

class Pieces(Sprite):
    def __init__(self):
        super().__init__()
        self.player_a_image =pygame.image.load('images/player_A.png')
        self.player_b_image =pygame.image.load('images/player_B.png')
        self.rect_a = self.player_a_image.get_rect()
        self.rect_b = self.player_a_image.get_rect()
        self.rect_a_width = self.rect_a.width
        self.rect_a_hight = self.rect_a.height

    def 画棋子(self,screen, x, y):
        self.rect_a.center = (x, y)
        screen.blit(self.player_a_image, self.rect_a)
    

        
