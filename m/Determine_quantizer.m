function [region]=Determine_quantizer(m, S, N)

    j = 2;
    temp_region(1) = m;
    for i = [1 3:2:N-1]
        x_inter = fsolve(@(x)(1+erf((x - m) / (S * 2^(1/2)))) / 2 - 1/2 - i/(2*N), temp_region(j - 1));
        
        temp_region(j) = x_inter;
        j = j + 1;
        
        test = 1 - (1 + erf((x_inter - m) / (S * 2^(1/2)))) / 2;
        if test < 1/N
            disp('REGION');
            disp(N);
            disp(test)
            break
        end
    end
    
    temp_region = temp_region(2:j-1);
    temp_region_2 = 2 * m - temp_region;
    
    region = [-inf temp_region_2(end:-1:1) temp_region inf];
end