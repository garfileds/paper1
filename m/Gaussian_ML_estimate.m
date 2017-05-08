function [m_hat, S_hat]=Gaussian_ML_estimate(X)

[l, N] = size(X);
m_hat = (1/N) * sum(X);

S_hat = zeros(1);
for k = 1:N
    S_hat = S_hat + (X(:,k) - m_hat) * (X(:,k) - m_hat)';
end
S_hat = (1/N) * S_hat;
end