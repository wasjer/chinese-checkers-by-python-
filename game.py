import pygame
import sys

from settings import Settings


class Chess():
    def __init__(self):
        pygame.init()
        self.game_active = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("中国跳棋")
        self.screen_rect = self.screen.get_rect()
        self.play_button = Button (self, "PLAY",self.screen_rect.centerx,self.screen_rect.centery)
        
    def _bgm(self):
        # 加载音效和背景音乐
        pygame.mixer.init()

        self.button_click = pygame.mixer.Sound('sound/laser.flac')
        self.bgm =pygame.mixer.music.load('sound/bgm.mp3')
        self.explosion_effect = pygame.mixer.Sound('sound/explosion.mp3')
        self.ship_hit_effect = pygame.mixer.Sound('sound/ship_hit.wav')
        self.explosion_effect.set_volume(0.3)
        self.ship_hit_effect.set_volume(0.2)
        
        self.play = pygame.mixer.music.play()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 检查用户操作
            self._check_events()
            # 播放BGM
            self._bgm.play()
            if self.game_active:
                pass
            # 更新屏幕
            self._update_screen()
            # 设置游戏的帧率
            self.clock.tick(self.settings.fps)


    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # elif event.type == pygame.KEYDOWN:
                #     self._check_keydown_events(event)
                # elif event.type == pygame.KEYUP:
                #     self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     self.mouse_pos = pygame.mouse.get_pos()
                     self._check_button(self.mouse_pos)
                     self._check_pieces(self.mouse_pos)

    def _check_pieces(self.mouse_pos):
        pass

    def _check_button(self,mouse_pos):
        """按下play，重新开始，一切重置"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        over_button_clicked = self.over_button.rect.collidepoint(mouse_pos)
        save_button_clicked = self.save_button.rect.collidepoint(mouse_pos)
        surrender_button_clicked = self.surrender_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.game_active:
            self.button_click.play()
            self._game_start()
        if over_button_clicked and self.game_active:
            self.button_click.play()
            sys.exit()
        if save_button_clicked and self.game_active:
            self.button_click.play()
            self._game_save()
        if surrender_button_clicked and self.game_active:
            self.button_click.play()
            self._game_surrender()

    def _game_save(self):
        pass
    def _game_surrender(self):
        pass
            
    def _game_start(self):
        self.game_active = True

                
    def _check_keydown_events (self, event):
        """响应按下"""

        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p and not self.game_active:
            self._game_start()



    def _update_screen(self):
        # 每次循环前都重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        draw_board()
        draw_pieces()
        draw_buttons()

        pygame.display.flip()        


def draw_board(screen):
    # 在这里绘制棋盘
    pass

def draw_pieces(screen):
    # 在这里绘制棋子
    pass
def draw_buttons(screen):
    # 绘制按钮
    pass