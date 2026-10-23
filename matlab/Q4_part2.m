clear; clc; close all;

t = linspace(0, 2*pi, 2000);

x_double = 15 * sin(3*t);
y_double = 15 * sin(2*t);

t_single = single(t);
x_single = single(15) * sin(single(3)*t_single);
y_single = single(15) * sin(single(2)*t_single);

t_half = half(t);
x_half = half(15) * sin(half(3)*t_half);
y_half = half(15) * sin(half(2)*t_half);

fraction_lengths = [1, 3, 6, 12]; 
Fm = fimath('RoundingMethod', 'Floor', 'OverflowAction', 'Saturate');

figure('Name', 'CNC Path: Floating-Point Comparison', 'Position', [100, 100, 800, 600]);
plot(x_double, y_double, 'k', 'LineWidth', 3); hold on;
plot(x_single, y_single, 'b--', 'LineWidth', 1.5);
plot(double(x_half), double(y_half), 'r:', 'LineWidth', 1.5);

title('CNC Lissajous Path: Floating-Point Precision');
xlabel('X Position (cm)'); ylabel('Y Position (cm)');
legend('Double (Ideal)', 'Single (32-bit)', 'Half (16-bit)');
grid on; axis equal;

figure('Name', 'CNC Path: Fixed-Point Quantization Effect', 'Position', [150, 150, 1000, 800]);

for i = 1:length(fraction_lengths)
    FL = fraction_lengths(i);
    WL = 6 + FL; 
    
    T = numerictype(1, WL, FL);
    
    x_fixed = fi(x_double, T, Fm);
    y_fixed = fi(y_double, T, Fm);
    
    subplot(2, 2, i);
    plot(x_double, y_double, 'k', 'LineWidth', 1.5); hold on;
    plot(double(x_fixed), double(y_fixed), 'r.-', 'MarkerSize', 6, 'LineWidth', 0.5);
    
    title(sprintf('Fixed-Point Q5.%d (Word Length = %d)', FL, WL));
    xlabel('X Position'); ylabel('Y Position');
    legend('Ideal Path', 'Fixed-Point Path', 'Location', 'best');
    grid on; axis equal;
end