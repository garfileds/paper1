file = '../data/rr/RR_e0607_MLIII_normalFit.txt';
entroy = 5;

data_g_raw = textread(file, '%d', 'delimiter', '\n');
data_g = data_g_raw / 1000;

param_g = mle(data_g');
m_g = param_g(1);
S_g = param_g(2);

fid = fopen('../data/entroyWitness.txt', 'a+');
for j = 2:1:floor(entroy)
    result = Determine_quantizer(m_g, S_g, 2.^j);
    fprintf(fid, [file, ' b=', num2str(j), '\n']);
    fprintf(fid, [mat2str(result), '\n\n']);
end
fclose(fid);