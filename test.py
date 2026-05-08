import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

# --- 配置色彩 ---
# 使用一组更有层次感的绿色
tree_colors = ["#1a472a", "#2d5a27", "#4a7c3a", "#7fb06f", "#a3c998"]
bg_color = "#f8f8f4" # 极淡的米灰色背景，让雪花可见

fig, ax = plt.subplots(figsize=(6, 10))
ax.set_facecolor(bg_color)
fig.patch.set_facecolor(bg_color)

# --------------------------
# 改进后的树冠生成函数 (填充式)
# --------------------------
def draw_dense_layer(ax, cx, cy, width, height, num_points=2000):
    # 在矩形范围内生成随机点
    x = np.random.uniform(cx - width/2, cx + width/2, num_points)
    # 使用 beta 分布让点更集中在三角形底部，制造厚重感
    y_dist = np.random.beta(2, 1, num_points)
    y = cy + height * y_dist
    
    # 计算三角形边界
    slope = (height * 0.9) / (width / 2)
    boundary_y = cy + height - slope * np.abs(x - cx)

    # 筛选出在三角形内部的点
    mask = y <= boundary_y
    x_fill = x[mask]
    y_fill = y[mask]
    
    # 添加随机扰动
    jitter_x = np.random.normal(0, 0.1, len(x_fill))
    jitter_y = np.random.normal(0, 0.1, len(y_fill))
    
    # 随机选择颜色和大小
    colors = np.random.choice(tree_colors, len(x_fill), p=[0.1, 0.2, 0.3, 0.3, 0.1])
    sizes = np.random.uniform(10, 40, len(x_fill))
    
    # 绘制基础层
    ax.scatter(x_fill + jitter_x, y_fill + jitter_y, s=sizes, c=colors, alpha=0.3, edgecolors='none')

# --------------------------
# 绘制树干
# --------------------------
for _ in range(250):
    jitter = np.random.normal(0, 0.08, 2)
    x = np.random.uniform(-0.6, 0.6) + jitter[0]
    y = np.random.uniform(-2.8, 0.2) + jitter[1] 
    # 树干颜色
    c_idx = int(np.abs(x) * 3)
    c = ["#4a3228", "#5c4033", "#6d4e3f"][min(c_idx, 2)]
    ax.scatter(x, y, s=np.random.uniform(30, 60), color=c, alpha=0.5, edgecolors='none')

# --------------------------
# 绘制树冠 (三层)
# --------------------------
layers = [
    (0, 0.5, 7.5, 5),   # 底层
    (0, 3.5, 6.5, 4.5), # 中层
    (0, 6.0, 5.0, 4.0), # 顶层
]

for cx, cy, w, h in layers:
    draw_dense_layer(ax, cx, cy, w, h, num_points=3500)


# --------------------------
# 装饰球
# --------------------------
ornament_colors = ["#d42426", "#e6b800", "#f0e68c", "#ff4500"] 

ornament_positions = [
    (0, 7.5), (-0.8, 6.8), (0.8, 6.8), 
    (-1.5, 5.0), (0, 5.2), (1.5, 5.0), (-0.5, 4.2), 
    (-2.2, 2.5), (-1.0, 3.0), (1.0, 3.0), (2.2, 2.5), (0, 1.8), 
    (-1.8, 1.0), (1.8, 1.0)
]

for (ox, oy) in ornament_positions:
    base_color = np.random.choice(ornament_colors)
    ax.add_patch(Circle((ox, oy), 0.35, color=base_color, alpha=0.1))
    ax.add_patch(Circle((ox, oy), 0.22, color=base_color, alpha=0.8))
    ax.add_patch(Circle((ox - 0.05, oy + 0.05), 0.05, color="white", alpha=0.6))

# --------------------------
# 顶星
# --------------------------
ax.scatter(0, 9.2, s=500, marker='*', color="#ffd700", zorder=10)
ax.scatter(0, 9.2, s=200, marker='*', color="#ffec8b", zorder=10)


# --------------------------
# 飘雪和积雪 (这里是修复后的代码)
# --------------------------
# 背景雪
for _ in range(300):
    x = np.random.uniform(-5, 5)
    y = np.random.uniform(-4, 11)
    ax.scatter(x, y, s=np.random.uniform(5, 30), color="white", alpha=0.4, edgecolors='none')

# 树上的积雪
for cx, cy, w, h in layers:
    snow_x = np.random.uniform(cx - w/2.5, cx + w/2.5, 200)
    snow_y = np.random.uniform(cy + h*0.5, cy + h*0.9, 200)
    
    # 修正变量名
    slope = (h * 0.9) / (w / 2)
    boundary_y = cy + h - slope * np.abs(snow_x - cx)
    
    mask = (snow_y <= boundary_y + 0.2) 
    
    ax.scatter(snow_x[mask], snow_y[mask], s=np.random.uniform(5, 15), color="white", alpha=0.5, zorder=5)


# --------------------------
# 文字
# --------------------------
ax.text(0, 10.8, "芋爱.的圣诞树", ha="center", fontsize=26, fontweight="bold", color="#333333")
ax.text(0, 10.0, "2025/12/25, create by Drop", ha="center", fontsize=12, color="#555555")
ax.text(0, -3.8, "Merry Christmas!", ha="center", fontsize=48,
        color="#cca300", alpha=0.9, fontweight="bold")

ax.set_xlim(-5, 5)
ax.set_ylim(-4, 11.5)
ax.axis("off")

plt.tight_layout()
plt.show()