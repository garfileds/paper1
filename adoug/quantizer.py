#-*- coding: utf-8 -*-

# Python实现正态分布

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math

# 绘制正态分布概率密度函数
u = 0
u01 = -2
sig02 = math.sqrt(1)
x_02 = np.linspace(u - 4, u + 4, 100)
y_sig02 = np.exp(-(x_02 - u) ** 2 / (2 * sig02 ** 2)) / (math.sqrt(2 * math.pi) * sig02)
plt.plot(x_02, y_sig02, "#000000", linewidth=2)
ax = plt.gca()
ax.spines['top'].set_position(('data', 0.4))
ax.spines['right'].set_position(('data', 4))
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', -4))

# 直方图
offset = 1.425
X_bar = np.array([-4 + offset, -1.15 + offset, -0.32 + offset, 0.32 + offset, 1.15 + offset])
# X_bar = np.array([-3.2, -1.6, -0, 1.6, 3.2])
Y_bar = np.array([0.4, 0.4, 0.4, 0.4, 0.4])
width_bar = np.array([2.85, 0.83, 0.64, 0.83, 2.85])
color_bar = ['#ffffff', '#9ca09c', '#ffffff', '#9ca09c', '#ffffff']
plt.bar(X_bar, Y_bar, width=3, color=color_bar, edgecolor="#000000")

# 区域标记
plt.annotate('00', xy=(-2.575, 0.2), xytext=(-2.8, 0.2))
plt.annotate('01', xy=(-2.575, 0.2), xytext=(-0.9, 0.2))
plt.annotate('11', xy=(-2.575, 0.2), xytext=(-0.2, 0.2))
plt.annotate('10', xy=(-2.575, 0.2), xytext=(0.5, 0.2))
plt.annotate('00', xy=(-2.575, 0.2), xytext=(2.5, 0.2))

# 坐标轴标记
plt.xlabel('Variable Space')
plt.ylabel('Probability Density')

plt.xlim(-4, 4)
plt.ylim(0, 0.4)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

plt.show()