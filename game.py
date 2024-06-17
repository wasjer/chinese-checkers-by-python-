import pygame
import sys
import math


class Grid():
    def __init__(self):
        self.grid_pos = []
        self.grid_473 = []


    def 建立所有的格子坐标列表(self, screen_width = 800, screen_height = 800):
        for j in range (-4,5):
            for i in range (-4,5):
                self.grid_pos.append((i,j))

        for x in range(4,9):
            for y in range(-4,1-(x-4)):
                self.grid_pos.append((x,y))
                self.grid_pos.append((-x,-y))
        for x in range(-4,1):
            for y in range(4,9-(4+x)):
                self.grid_pos.append((x,y))
                self.grid_pos.append((-x,-y))
        self.grid_pos = list(set(self.grid_pos))


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
        self.选中的圆圈 = None # 添加一个变量来存储圆的位置
        self.turn = 0
        self.grid = Grid()
        self.grid.建立所有的格子坐标列表()
        self.grid_stat = {}
        self.grid_to_blit = {}
        self.grid_to_stat = {}
        self.上一个有效选中 = []
        self.possible_moves = []
        self.建立格子字典并初始化()
        self.blue = False
        self.red = False
    
    def 建立格子字典并初始化(self):
        """建立格子状态字典，并制作像素坐标和轴坐标的互译字典"""
        # "2":"没有棋子"
        # "0":"红色棋子"
        # "1":"蓝色棋子"
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
        # 上方是红棋，下方是蓝棋
        for key, value in self.grid_stat.items():
            if key[1] > 4:
                self.grid_stat[key] = 0
        for key, value in self.grid_stat.items():
            if key[1] < -4:
                self.grid_stat[key] = 1
        # self.仅测试用()

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
        clicked_circle = self._检查点击位置是否在格子内(mouse_x, mouse_y)
     
        if clicked_circle:
            stat = self.grid_stat[self.grid_to_stat[clicked_circle]]
            if stat == self.turn:
                self.grid_stat = {k: (v if v != 3 else 2) for k, v in self.grid_stat.items()} # 把所有空白格回复成2
                self.选中的圆圈 = clicked_circle     # 用来显示选中标记的变量
                self.根据规则判断选中子的可走格(self.grid_to_stat[clicked_circle])
                self.上一个有效选中.append(clicked_circle)
            elif stat == 3 :   
                last_selected = self.上一个有效选中.pop()
                self.grid_stat[self.grid_to_stat[clicked_circle]] = self.grid_stat[self.grid_to_stat[last_selected]] 
                self.grid_stat[self.grid_to_stat[last_selected]] = 2 # 点击可走格，则可走格变成棋子，原来格子变成空格
                self.turn = 1 - self.turn  # 轮到对方走棋
                self.选中的圆圈 = None # 清空选择
                self.grid_stat = {k: (v if v != 3 else 2) for k, v in self.grid_stat.items()} # 把所有空白格回复成2
                print(f"Moved piece from {self.grid_to_stat[last_selected]} to {self.grid_to_stat[clicked_circle]}")
                self._检查是否胜利()

    def _检查点击位置是否在格子内(self,mouse_x, mouse_y):
         for (cx, cy) in self.grid_to_stat.keys():
            distance = math.sqrt((mouse_x - cx) ** 2 + (mouse_y - cy) ** 2)   # 计算点击位置到圆心的距离
            if distance <= 11 :  # 假设半径为11
                return (cx,cy)

    def 根据规则判断选中子的可走格(self, pos, visited=None, is_jump=False):
        """用递归调用，深度优先遍历，找出选中棋子的所有可走位置"""
        if visited is None:   # 首次执行方法时建立集合visited，后面调用时就继承之前的visited
            visited = set()

        x, y = pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)] # 格子的6个方向

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in self.grid_stat and self.grid_stat[(new_x, new_y)] == 2 and not is_jump: # 棋子的相邻格可以走，但跳子落点的相邻格不能走
                self.possible_moves.append((new_x, new_y))
                self.grid_stat[(new_x, new_y)] = 3
            elif (new_x, new_y) in self.grid_stat and self.grid_stat[(new_x, new_y)] != 2:  # 相邻格如果有棋子，则沿着该方向检查下一个格子
                jump_x, jump_y = new_x + dx, new_y + dy
                if (jump_x, jump_y) in self.grid_stat and self.grid_stat[(jump_x, jump_y)] == 2: # 如果下一个是空格，则可以走。
                    self.possible_moves.append((jump_x, jump_y))
                    if (jump_x, jump_y) not in visited:  # 如果这个跳子落点不在集合内，就把他加进去，格子属性改成可以走
                        visited.add((jump_x, jump_y))
                        self.grid_stat[(jump_x, jump_y)] = 3
                        self.根据规则判断选中子的可走格((jump_x, jump_y), visited, is_jump=True)

        return visited  # 返回这个集合，直到所有可走的位置全部找出来，方法停止。

    def 更新屏幕显示(self):
        self.画棋盘()
        self.画棋子()
        self._在有效选中的棋子上显示圆圈()
        if self.red:
            self.胜利("red")
        if self.blue:
            self.胜利("blue")
        self.scr.blit(self.透明图层, (0,0)) #画上透明图层
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

    def _检查是否胜利(self):
        if all(self.grid_stat[key] == 1 for key in self.grid_stat if key[1] > 4):
            self.blue = True
            print ("蓝方胜利")
        if all(self.grid_stat[key] == 0 for key in self.grid_stat if key[1] < -4):
            self.red = True
            print ("红方胜利")

    def 仅测试用(self):
        for key, value in self.grid_stat.items():
            if key[1] > 4:
                self.grid_stat[key] = 1
            if key[1] < -4:
                self.grid_stat[key] = 0
        self.grid_stat[(4,-5)] = 2
        self.grid_stat[(4,-4)] = 0
        self.grid_stat[(-4,5)] = 2
        self.grid_stat[(-4,4)] = 1
        
    def 胜利(self, color):
        log = f"{color} is win"
        self.font = pygame.font.SysFont(None, 48)  # 使用默认字体
        self.font_image = self.font.render(log, True, (255, 0, 255))  # 渲染字体
        # 在透明图层上绘制字体
        text_rect = self.font_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.透明图层.blit(self.font_image, text_rect)

if __name__ == '__main__':
    role = Checkers()
    role.运行游戏()


