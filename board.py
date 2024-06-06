import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# 创建图形
fig, ax = plt.subplots()
ax.set_aspect('equal')
pos = []

def plot_rotated_triangles(length):
    center_x, center_y = 0, 0
    side_length = length

    # 计算第一个正三角形的三个顶点
    def triangle(side_length):
        h = math.sqrt(3) / 2 * side_length  # 高度
        triangle = [
            (center_x - side_length / 2, center_y - h / 3),
            (center_x + side_length / 2, center_y - h / 3),
            (center_x, center_y + 2 * h / 3)
        ]
        return triangle

    tri_1 = triangle(side_length)
    h = math.sqrt(3) / 2 * side_length  # 高度

    # 旋转矩阵
    def rotate_point(x, y, angle, cx, cy):
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        # 绕任一点的旋转公式，推导过程是先把这点平移到原点（x-cx）再旋转，再根据和差公式拆分合并，再平移回去+cx
        x_new = cos_angle * (x - cx) - sin_angle * (y - cy) + cx 
        y_new = sin_angle * (x - cx) + cos_angle * (y - cy) + cy
        return x_new, y_new

    # 旋转第一个正三角形的顶点60度
    angle = math.pi / 3  # 60度
    tri_2 = [rotate_point(x, y, angle, center_x, center_y) for x, y in tri_1]

    # 绘制第一个正三角形
    tri_1.append(tri_1[0])  # 添加第一个点到最后，形成闭合路径
    ax.plot([x for x, y in tri_1], [y for x, y in tri_1], 'k-', zorder=2)
    
    # 绘制第二个正三角形
    tri_2.append(tri_2[0])  # 添加第一个点到最后，形成闭合路径
    ax.plot([x for x, y in tri_2], [y for x, y in tri_2], 'k-', zorder=2)

    # 计算并绘制边上的圆点
    def plot_points_on_edge(triangle):
        num_points = side_length
        for i in range(3):  # 对于三角形的每一条边
            x1, y1 = triangle[i]
            x2, y2 = triangle[i+1]
            for j in range(1, num_points+1):  # 在每条边上分割为指定段数，共 num_points+1 个点
                t = j / num_points
                x = (1 - t) * x1 + t * x2
                y = (1 - t) * y1 + t * y2
                circle = patches.Circle((x, y), radius=0.25, edgecolor='black', facecolor='white', zorder=2)
                ax.add_patch(circle)
                pos.append([x, y])  # 记录圆心位置

    plot_points_on_edge(tri_1)
    plot_points_on_edge(tri_2)

    # 设置轴的限制
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)

plot_rotated_triangles(12)
plot_rotated_triangles(9)
plot_rotated_triangles(6)
plot_rotated_triangles(3)


circle = patches.Circle((0, 0), radius=0.25, edgecolor='black', facecolor='white', zorder=2)
ax.add_patch(circle)
pos.append([0,0])


x = [0,4,0,-4]
y = [7,0,-7,0]

x_60 = []
y_60 = []
y_120 = []
x_120 =[]
x_hexagon = [0,0,0,0,0,0]
y_hexagon = [0,0,0,0,0,0]

for i in [0, 1, 2, 3]:
    angle_60 = math.pi / 3
    cos_angle = math.cos(angle_60)
    sin_angle = math.sin(angle_60)
    xt = cos_angle * x[i] - sin_angle * y[i]
    yt = sin_angle * x[i] + cos_angle * y[i]
    x_60.append(xt)
    y_60.append(yt)

for i in [0, 1, 2, 3, ]:
    angle_120 = math.pi * 2 / 3
    cos_angle = math.cos(angle_120)
    sin_angle = math.sin(angle_120)
    xt = cos_angle * x[i] - sin_angle * y[i]
    yt = sin_angle * x[i] + cos_angle * y[i]
    x_120.append(xt)
    y_120.append(yt)

print(x_60)
print(y_60)
print(x_120)
print(y_120)

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
plt.fill(x,y, color='skyblue', alpha=1)
plt.fill(x_60,y_60, color='red', alpha=1)
plt.fill(x_120,y_120, color='green', alpha=1)
plt.fill(x_hexagon,y_hexagon, color='w', alpha=1)

# 绘制圆形中心之间的红色连接线
for i in range(len(pos)):
    for j in range(i + 1, len(pos)):
        x1, y1 = pos[i]
        x2, y2 = pos[j]
        # 判断两圆是否相邻
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if distance <= 1.5:  # 1.5 是相邻圆心的距离阈值，调整它来符合实际需要
            ax.plot([x1, x2], [y1, y2], 'k-', zorder=1)



plt.show()
