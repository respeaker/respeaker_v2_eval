% analyze the coherence between the last channel and other channels
% sudo apt-get install octave octave-signal

function coherence(wavefile)

[x, fs] = wavread(wavefile);

pkg load signal

channels = size(x, 2);

figure
hold on

colors = ['y', 'm', 'c', 'r', 'g', 'b', 'k', '.', '*'];

for i = 1:channels
    [P, f] = mscohere(x(:, i), x(:, 1), hamming(1024), [], 1024, fs);
    plot(f, P, colors(i))
end

legend('show')
