% 求g的pdf：MLEstimate
data_g_raw = textread('../data/rr/RR_e0103_MLIII_normalFit.txt', '%d', 'delimiter', '\n');
data_g = data_g_raw / 1000;

param_g = mle(data_g');
m_g = param_g(1);
S_g = param_g(2);

% [m_g, S_g] = Gaussian_ML_estimate(data_g');

% 确定quantizer
N = 64;

region = Determine_quantizer(m_g, S_g, N);

% 求（g, g'）的pdf：Parzen Guassian
[X_g1, X_g2] = textread('../data/sample/gg_e0103.txt', '%d %d', 'delimiter', '\n');
X = [X_g1 X_g2] / 1000;

h1 = 0.001;
h2 = 0.05;
num_region = length(region);
grid_g1 = [region(1):h2:region(2) region(2):h1:region(num_region - 1) region(num_region - 1):h2:region(num_region)];
grid_g2 = grid_g1;
[x_g1, x_g2] = meshgrid(grid_g1, grid_g2);
x_g1 = x_g1(:);
x_g2 = x_g2(:);
xi_gg = [x_g1 x_g2];

[pdf_gg, x_gg] = ksdensity(X, xi_gg);

pdf_gg_reshape = reshape(pdf_gg, length(grid_g1), length(grid_g2));

% 求量化后 g=g' 的概率：pdf（g, g'）积分
p_gg = 0;
start_point = 1;
for i = 1:length(region)-1
    if i == 1 || i == length(region) - 1
       hh = 0.05;
    else
        hh = 0.001;
    end
    
    range = region(i):hh:region(i+1);
    num_range = length(range);

    grid_g1_2 = grid_g1(start_point:start_point + num_range - 1);
    grid_g2_2 = grid_g1_2;
    pdfxx = pdf_gg_reshape(start_point:start_point + num_range - 1, start_point:start_point + num_range - 1);
    
    p_gg = p_gg + trapz(grid_g2_2, trapz(grid_g1_2, pdfxx, 2));
    
    start_point = start_point + num_range - 1;
end

% 求量化后 g=g' 的概率：计数
sum_gg = zeros(1, length(region) - 1);
X = X';
[d_gg, num_X] = size(X);

for i = 1:length(region)-1
    for j = 1:num_X
       if (X(1, j) < region(i+1) && X(1, j) >= region(i) && X(2, j) < region(i+1) && X(2, j) >= region(i))
           sum_gg(i) = sum_gg(i) + 1;
       end
    end
end

p_gg_2 = sum(sum_gg) / num_X;

% 求（g, i_g）的成功匹配概率：g与i_g同分布且为正态分布，独立
p_gi_g = 0;
for i = 1:length(region)-1
    pdf_gi_g = @(x, y)(2.* pi.* S_g.^2)^(-1) * exp((-1/2) .* ((x - m_g).^2 + (y - m_g).^2) / (S_g.^2));
    p_gi_g = p_gi_g + integral2(pdf_gi_g, region(i), region(i+1),region(i), region(i+1));
end

disp(p_gg);
disp(p_gg_2);
disp(sum_gg);
disp(p_gi_g);