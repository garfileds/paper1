x_inter = fsolve(@int_gauss, 1);
disp(x_inter);

function val=int_gauss(x)
    m = 1;
    S = 8;
    N = 16;
    i = 3;
    
    val = cdf('Normal', x, m, S) - 1/2 - i/2*N;
end

