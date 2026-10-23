
clear; clc; close all;


N = 100;
x = randn(1, N); 

h = [0.12, 0.25, 0.38, 0.5, 0.75, 1, 0.75, 0.5, 0.38, 0.25, 0.12];


y_float = conv(x, h);

fprintf('[Question 1] Floating-point output calculated successfully.\n\n');


N_fft = 512;
Y_float_fft = fft(y_float, N_fft);
mag_float = 20*log10(abs(Y_float_fft(1:N_fft/2)));
freq_axis = linspace(0, 1, N_fft/2);

fractional_bits = [1, 2, 3, 4];
integer_bits = 3;

fprintf('[Question 2 & 3] Fixed-point conversion and SAE calculation:\n');
fprintf('-------------------------------------------------\n');

figure('Name', 'FFT Comparison: Floating vs Manual vs Tool', 'Position', [100, 100, 1000, 700]);


% SAE Error
for i = 1:length(fractional_bits)
    f = fractional_bits(i);
    
    scale_factor = 2 ^ f;
    h_manual = round(h * scale_factor) / scale_factor;
    y_manual = conv(x, h_manual);
    sae_manual = sum(abs(y_float - y_manual));
    
    word_length = 1 + integer_bits + f; 
    
    h_tool_obj = fi(h, 1, word_length, f);
    h_tool = double(h_tool_obj);
    
    y_tool = conv(x, h_tool);
    sae_tool = sum(abs(y_float - y_tool));
    
    fprintf('>> Format Q3.%d (Fractional bits: %d)\n', f, f);
    fprintf('   [Manual Method] SAE Error : %.4f\n', sae_manual);
    fprintf('   [Tool Method]   SAE Error : %.4f\n', sae_tool);
    fprintf('-------------------------------------------------\n');
    
    % FFT 
    Y_manual_fft = fft(y_manual, N_fft);
    mag_manual = 20*log10(abs(Y_manual_fft(1:N_fft/2)));
    
    Y_tool_fft = fft(y_tool, N_fft);
    mag_tool = 20*log10(abs(Y_tool_fft(1:N_fft/2)));
    
    subplot(2, 2, i);
    plot(freq_axis, mag_float, 'b', 'LineWidth', 2); hold on;
    plot(freq_axis, mag_manual, 'r--', 'LineWidth', 1.5);
    plot(freq_axis, mag_tool, 'g:', 'LineWidth', 1.5);
    title(sprintf('[Question 4] Format Q3.%d FFT', f));
    xlabel('Normalized Frequency (\times \pi rad/sample)');
    ylabel('Magnitude (dB)');
    legend('Floating (Ideal)', 'Manual Fixed', 'Tool Fixed');
    grid on;
end

fprintf('\n[Question 4] FFT comparison plots generated successfully.\n');