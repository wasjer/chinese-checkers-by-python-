import pygame

class Settings:
    """储存所有游戏设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.fps = 60
        self.image_path='image.png'
        self.pos_path='pos_set.json'
