import matplotlib.pyplot as plt
import math

class Board:
    """这是一个制作棋盘的类"""

    def __init__(self):
        """初始化棋盘，需要参数的时候再加，并且默认值"""
        self.fig, self.ax= plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        # 隐藏边框
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.pos = []
        self.pos_available = []
        # self.piece = Pieces(self)
        self.available = False
   
    def 位置是否被占(self, x, y):
        for i in range(len(self.piece.piece_set)):
            x1, y1 = self.self.piece_set[i]
            if x1 == x and y1 == y:
                self.available = True
                break

    def _画三角形(self, side_length, center_x=0, center_y=0):
        """给定边长，计算正三角形的三个顶点的方法"""
        self.side_length = side_length
        h = math.sqrt(3) / 2 * self.side_length  # 高度
        triangle = [
            (center_x - side_length / 2, center_y - h / 3),
            (center_x + side_length / 2, center_y - h / 3),
            (center_x, center_y + 2 * h / 3)
        ]
        return triangle
   
    def _旋转点(self,x, y, angle, cx=0, cy=0):
            """按照给定角度旋转一个点的方法"""
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)
            x_new = cos_angle * (x - cx) - sin_angle * (y - cy) + cx
            y_new = sin_angle * (x - cx) + cos_angle * (y - cy) + cy
            return x_new, y_new
   
    def _画一个带圆圈的双三角形(self,length):
        self.length = length
        tri_1 = self._画三角形(length)
        angle = math.pi / 3  # 60度
        tri_2 = [self._旋转点(x, y, angle) for x, y in tri_1]
        # 绘制第一个正三角形
        tri_1.append(tri_1[0])  # 添加第一个点到最后，形成闭合路径
        # self.ax.plot([x for x, y in tri_1], [y for x, y in tri_1], 'k-', zorder=2, linewidth=0.5)
        # 绘制第二个正三角形
        tri_2.append(tri_2[0])  # 添加第一个点到最后，形成闭合路径
        # self.ax.plot([x for x, y in tri_2], [y for x, y in tri_2], 'k-', zorder=2, linewidth=0.5)
        self._画圆圈(tri_1)
        self._画圆圈(tri_2)
            # 设置轴的限制
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
   
    def _画圆圈(self,triangle):
        """计算并绘棋盘上的上的圆圈"""
        num_points = self.side_length
        for i in range(3):  # 对于三角形的每一条边
            x1, y1 = triangle[i]
            x2, y2 = triangle[i+1]
            for j in range(1, num_points+1):  # 在每条边上分割为指定段数，共 num_points+1 个点
                t = j / num_points
                x = (1 - t) * x1 + t * x2
                y = (1 - t) * y1 + t * y2
                xr = round(x, 2)
                yr = round(y, 2)
                circle = plt.Circle((xr, yr), radius=0.25, edgecolor='black', facecolor='white', zorder=2)
                self.ax.add_patch(circle)
                self.pos.append((xr, yr))  # 记录圆心位置
        self.pos.append((0,0))
        self.pos_set = list(set(bo.pos))
   
    def _画线格(self):
        self._画一个带圆圈的双三角形(12)
        self._画一个带圆圈的双三角形(3)
        self._画一个带圆圈的双三角形(9)
        self._画一个带圆圈的双三角形(6)
        circle = plt.Circle((0, 0), radius=0.25, edgecolor='black', facecolor='white', zorder=2)
        self.ax.add_patch(circle)
   
    def _涂颜色(self):
        y = [self.pos_set[14][1],self.pos_set[0][1],self.pos_set[41][1],self.pos_set[49][1]]
        x = [self.pos_set[14][0],self.pos_set[0][0],self.pos_set[41][0],self.pos_set[49][0]]
        x_60 = []
        y_60 = []
        y_120 = []
        x_120 = []
        x_hexagon = [0, 0, 0, 0, 0, 0]
        y_hexagon = [0, 0, 0, 0, 0, 0]
        for i in list(range(0,4)):
            angle_60 = math.pi / 3
            cos_angle = math.cos(angle_60)
            sin_angle = math.sin(angle_60)
            xt = cos_angle * x[i] - sin_angle * y[i]
            yt = sin_angle * x[i] + cos_angle * y[i]
            x_60.append(xt)
            y_60.append(yt)
        for i in list(range(0,4)):
            angle_120 = math.pi * 2 / 3
            cos_angle = math.cos(angle_120)
            sin_angle = math.sin(angle_120)
            xt = cos_angle * x[i] - sin_angle * y[i]
            yt = sin_angle * x[i] + cos_angle * y[i]
            x_120.append(xt)
            y_120.append(yt)

        x_hexagon[0] = x_120[1]
        x_hexagon[1] = x_60[1]
        x_hexagon[2] = x[1]
        x_hexagon[3] = x_120[3]
        x_hexagon[4] = x_60[3]
        x_hexagon[5] = x[3]

        y_hexagon[0] = y_120[1]
        y_hexagon[1] = y_60[1]
        y_hexagon[2] = y[1]
        y_hexagon[3] = y_120[3]
        y_hexagon[4] = y_60[3]
        y_hexagon[5] = y[3]

        # 使用 fill 填充颜色
        plt.fill(x, y, color='skyblue', alpha=1)
        plt.fill(x_60, y_60, color='red', alpha=1)
        plt.fill(x_120, y_120, color='green', alpha=1)
        plt.fill(x_hexagon, y_hexagon, color='w', alpha=1)
   
    def _画线(self):
        """绘制圆形中心之间的连接线"""
        for i in range(len(self.pos_set)):
            for j in range(i + 1, len(self.pos_set)):
                x1, y1 = self.pos_set[i]
                x2, y2 = self.pos_set[j]
                # 判断两圆是否相邻
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance <= 1.5:  # 1.5 是相邻圆心的距离阈值，调整它来符合实际需要
                    self.ax.plot([x1, x2], [y1, y2], 'k-', zorder=1, linewidth=0.7)

    def _计算相邻格(self, x_select, y_select, radius=1.5):
        for i in range(len(self.pos_set)):
            x1, y1 = self.pos_set[i]
            # 判断两圆是否相邻
            distance = math.sqrt((x_select - x1) ** 2 + (y_select - y1) ** 2)
            if distance <= radius:  # 1.5 是相邻圆心的距离阈值，调整它来符合实际需要
                self.pos_available.append(x1,y1)
   
    def _计算间隔格(self, x_select, y_select,radius=1.5):
        self._计算相邻格(x_select,y_select)
        for i in range(len(self.pos_set)):
            x_unavail, y_unavail = self.pos_set[i]
            # 判断两圆是否相邻
            distance = math.sqrt((x_select - x_unavail) ** 2 + (y_select - y_unavail) ** 2)
            if distance <= radius and not self.available:  # 1.5 是相邻圆心的距离阈值，调整它来符合实际需要
# TODO: 这一大串公式是判断相邻格被占时，这个方向的间隔格坐标。我感觉应该可以简化下面这一大串。
                if y_unavail == y_select:
                    if x_select > x_unavail:
                        x = x_unavail - (x_select - x_unavail) 
                        y = y_select
                    elif x_select < x_unavail:
                        x = x_unavail + (x_unavail - x_select)
                        y = y_select
                if y_unavail > y_select:
                    if x_select < x_unavail:
                        x = x_unavail + (x_unavail - x_select) 
                        y = y_unavail + (y_unavail - y_select)
                    elif x_select > x_unavail:
                        x = x_unavail - (x_select - x_unavail)
                        y = y_unavail + (y_unavail - y_select)
                if y_unavail < y_select:
                    if x_select < x_unavail:
                        x = x_unavail + (x_unavail - x_select) 
                        y = y_unavail - (y_select - y_unavail)
                    elif x_select > x_unavail:
                        x = x_unavail - (x_select - x_unavail)
                        y = y_unavail - (y_select - y_unavail)
                self.pos_available.append(x,y)
# TODO:这后面都放到主程序里就行了  
bo = Board()
bo._画线格()
bo._涂颜色()
bo._画线()
plt.show()
# plt.savefig('image.png', dpi=600, bbox_inches='tight')  # 提高DPI，保存高分辨率图像，并移除留白

# # 保存pos_unique列表到JSON文件
# with open('pos_set.json', 'w') as f:
#     json.dump(bo.pos_set, f)

