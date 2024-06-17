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



