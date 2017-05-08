function [px]=Parzen_gauss_kernel(X, h, x_left_limit, x_right_limit)

x_g1 = x_left_limit:h:x_right_limit;
x_g2 = x_left_limit:h:x_right_limit;

[X1, X2] = meshgrid(x_g1, x_g2);
[d_g, N_g] = size(X1);

[d, N] = size(X);

for i = 1:N_g
   for j = 1:N_g
       px(i, j) = 0;
       for k = 1:N
          xi = X(:, k);
          px(i, j) = px(i, j) + exp(-([X1(i,j) X2(i,j)]' - xi)' * ([X1(i,j) X2(i,j)]' - xi) / (2 * h^2));
       end
       px(i, j) = px(i, j) * (1/N) * (1/((2 * pi)^(d/2) * (h^d)));
   end
end
end