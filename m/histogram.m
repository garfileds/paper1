% 导入数据
load rr1.txt
% 调用ecdf函数计算xc处的经验分布函数值f_ecdf
[f_ecdf, xc] = ecdf(rr1);
% 新建图形窗口，然后绘制频率直方图，直方图对应7个小区间
figure;
ecdfhist(f_ecdf, xc, 97);
hold on;
xlabel('IPI');  % 为X轴加标签
ylabel('Frequency');  % 为Y轴加标签

% 调用ksdensity函数进行核密度估计
% [f_ks1,xi1,u1] = ksdensity(rr);
% 绘制核密度估计图，并设置线条为黑色实线，线宽为3
% plot(xi1,f_ks1,'r','linewidth',2)

xi1 = 900:1:1300;

ms = mean(rr1);  % 计算x的平均值
ss = std(rr1);  % 计算x的标准差
% 计算xi1处的正态分布密度函数值，正态分布的均值为ms，标准差为ss
f_norm = normpdf(xi1,ms,ss); 
% 绘制正态分布密度函数图，并设置线条为红色点划线，线宽为3
ax = plot(xi1,f_norm,'r','linewidth',2);
% set(handles, 'xtick', 800:200:1400);

% 为图形加标注框，标注框的位置在坐标系的左上角
% legend('频率直方图','核密度估计图', '正态分布密度图', 'Location','NorthWest')