clear; clc; close all;

order_filter = 6;
cutoff_freq = 0.4;
[b, a] = butter(order_filter, cutoff_freq);

sosm = tf2sos(b, a);

N_samples = 5000;
x = rand(1, N_samples) - 0.5;

Hd_ideal = dfilt.df2sos(sosm);
y_ideal = filter(Hd_ideal, x);

window_size = 50;
Y_ideal_fft = abs(fft(y_ideal));
Y_ideal_smooth = movmean(Y_ideal_fft(1:N_samples/2), window_size);
freq_axis = linspace(0, 1, N_samples/2);

norms = {'l1', 'L1', 'l2', 'linf', 'Linf'};
orders = {'up', 'down'};

figure('Name', 'Fixed-Point SoS Filter: Norm and Order Comparison', 'Position', [50, 50, 1400, 800]);
plot_idx = 1;

for i = 1:length(norms)
    for j = 1:length(orders)
        current_norm = norms{i};
        current_order = orders{j};
        
        Hd_fixed = dfilt.df2sos(sosm);
        Hd_fixed.Arithmetic = 'fixed';
        
        scale(Hd_fixed, current_norm, 'sosreorder', current_order);
        
        y_fixed_obj = filter(Hd_fixed, x);
        y_fixed = double(y_fixed_obj); 
        
        sae_error = sum(abs(y_ideal - y_fixed));
        fprintf('Norm: %-4s | Order: %-4s | SAE Error: %.4f\n', current_norm, current_order, sae_error);
        
        Y_fixed_fft = abs(fft(y_fixed));
        Y_fixed_smooth = movmean(Y_fixed_fft(1:N_samples/2), window_size);
        
        subplot(5, 2, plot_idx);
        plot(freq_axis, 20*log10(Y_ideal_smooth), 'b', 'LineWidth', 1.5); hold on;
        plot(freq_axis, 20*log10(Y_fixed_smooth), 'r--', 'LineWidth', 1.2);
        
        title(sprintf('Norm: %s, Order: %s', current_norm, current_order));
        if plot_idx >= 9
            xlabel('Normalized Frequency (\times \pi rad/sample)');
        end
        ylabel('Magnitude (dB)');
        grid on;
        
        if plot_idx == 1
            legend('Ideal (Float)', 'Fixed-Point');
        end
        
        plot_idx = plot_idx + 1;
    end
end
fprintf('          Plots generated successfully.          \n');