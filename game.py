# TODO: 我添加了一个测试点击位置画圆并返回坐标的方法，但没有显示我画的圆，而且返回的坐标也和pos_set中差的很远。
import pygame
import sys
from pieces import Pieces
from grid import Grid
import math


class Checkers:
    """管理游戏资源和行为的类"""
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 800
        self.game_active = False
        self.scr = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption("中国跳棋")
        self.board_image = pygame.image.load("D:\\garage\\learning\\python_work\\chinese jump checkers\\image.png")         # 加载背景图片
        self.board_rect = self.board_image.get_rect()
        self.平滑缩小的棋盘图 = pygame.transform.smoothscale(self.board_image,(self.screen_width,self.screen_height))
        self.透明图层 = pygame.Surface((self.screen_width,self.screen_height), pygame.SRCALPHA)
        self.pieces = Pieces()
        self.选中的圆圈 = None # 添加一个变量来存储圆的位置
        self.step = 0
        self.turn = 0
        self.grid = Grid()
        self.grid.建立所有的格子坐标列表()
        self.grid_stat = {}
        self.grid_to_blit = {}
        self.grid_to_stat = {}
        self.上一个有效选中 = None
        self.建立格子字典并初始化()
        self.grid_explain = {
            "0":"没有棋子",
            "1":"红色棋子",
            "2":"蓝色棋子",
        }
    
    def 建立格子字典并初始化(self):
        for i in range(len(self.grid.grid_pos)):
            self.grid_stat[(self.grid.grid_pos[i])] = 2
            a = self.grid.grid_pos[i][0]
            b = self.grid.grid_pos[i][1]
            self.grid_to_blit[self.grid.grid_pos[i]] = (
                round((47.3 * (a + (b / 2))), 2) + self.screen_width/2,
                round(self.screen_height/2 - (47.3 * math.sqrt(3) / 2 * b), 2)
                )
            self.grid_to_stat[(
                round((47.3 * (a + (b / 2))), 2) + self.screen_width/2,
                round(self.screen_height/2 - (47.3 * math.sqrt(3) / 2 * b), 2)
            )] = self.grid.grid_pos[i]

        for key, value in self.grid_stat.items():
            if key[1] > 4:
                self.grid_stat[key] = 0
        for key, value in self.grid_stat.items():
            if key[1] < -4:
                self.grid_stat[key] = 1
        # for key, value in self.grid_for_blit.items():
        #     print(f'{key}: {value}')
        # for key, value in self.grid_for_stat.items():
        #     print(f'{key}: {value}')

    def 运行游戏(self):
        """开始游戏的主循环"""
        while True:
            self.检查事件()
            self.更新屏幕显示()

    def 检查事件(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_pos = pygame.mouse.get_pos()     # 获取鼠标点击位置
                self._检查左键点击(event.pos)
                
    def _检查左键点击(self,pos):
        mouse_x, mouse_y = pos
        # check = self.selected.pop()
        for (cx, cy), data in self.grid_to_stat.items():
            distance = math.sqrt((mouse_x - cx) ** 2 + (mouse_y - cy) ** 2)   # 计算点击位置到圆心的距离
            if distance <= 11 :  # 假设半径为11
                print(f"Clicked inside circle at ({cx}, {cy}) with data: {data}")  # 测试
                print(self.grid_stat[data])  # 测试
                self.选中的圆圈 = (cx, cy)
                self.上一个有效选中 = (cx, cy)
            # elif distance <= 11 and (cx,cy) != check:
            #     self.grid_stat[(cx,cy)] = self.turn
            #     self.grid_stat[check] = 2
            #     self.turn = 1- self.turn


    def 更新屏幕显示(self):
        self.画棋盘()
        self.画棋子()
        self._在有效选中的棋子上显示圆圈()
        self.scr.blit(self.透明图层, (0,0),) #画上透明图层
        # self.检验格子坐标()
        pygame.display.flip() # 每次循环前都重新绘制屏幕

    def 画棋盘(self):
        self.scr.blit(self.平滑缩小的棋盘图, (0,0),)
        self.透明图层.fill((0, 0, 0, 0)) 

    def 画棋子 (self):
        for key, value in self.grid_stat.items():
            if value == 0:
                pygame.draw.circle(self.scr, (255, 0, 0), self.grid_to_blit[key], 14)  # 绘制红色圆圈
            elif value == 1:
                pygame.draw.circle(self.scr, (0, 0, 255), self.grid_to_blit[key], 14)  # 绘制红色圆圈
                    
    def _在有效选中的棋子上显示圆圈(self):
        if self.选中的圆圈:
            if self.grid_stat[self.grid_to_stat[self.选中的圆圈]] == self.turn:
                self.透明图层.fill((0, 0, 0, 0))
                pygame.draw.circle(self.透明图层, (255,255,255, 150), self.选中的圆圈, 11, 2)  # 绘制选中圆圈

    def 检验格子坐标(self):
        for key in self.grid_to_blit.keys():
            pygame.draw.circle(
                self.scr, 
                (255, 0, 0), 
                key, 
                14)  # 绘制红色圆圈
            
if __name__ == '__main__':
    role = Checkers()
    role.运行游戏()



