clear; clc; close all;

t_float = linspace(0, 2*pi, 1000);

x_ideal = 15 * sin(3*t_float);
y_ideal = 15 * sin(2*t_float);

th_x_float = wrapToPi(3 * t_float);
th_y_float = wrapToPi(2 * t_float);

FL_array = [4, 8, 11, 15]; 
MSE_results = zeros(1, length(FL_array));

Fm = fimath('RoundingMethod', 'Floor', 'OverflowAction', 'Saturate');

figure('Name', 'CNC Path: Maclaurin Fixed-Point Integration', 'Position', [100, 100, 1000, 800]);

for i = 1:length(FL_array)
    FL = FL_array(i);
    WL = 8 + FL; 
    T = numerictype(1, WL, FL);
    
    th_x_fi = fi(th_x_float, T, Fm);
    th_y_fi = fi(th_y_float, T, Fm);
    
    c_sin = fi([1/factorial(9), 1/factorial(7), 1/factorial(5), 1/factorial(3), 1], T, Fm);
    
    x2_fi = th_x_fi .* th_x_fi;
    y2_fi = th_y_fi .* th_y_fi;
    
    sin_x_fi = th_x_fi .* (c_sin(5) - x2_fi .* (c_sin(4) - x2_fi .* (c_sin(3) - x2_fi .* (c_sin(2) - x2_fi .* c_sin(1)))));
    sin_y_fi = th_y_fi .* (c_sin(5) - y2_fi .* (c_sin(4) - y2_fi .* (c_sin(3) - y2_fi .* (c_sin(2) - y2_fi .* c_sin(1)))));
    
    x_fixed = fi(15 * sin_x_fi, T, Fm);
    y_fixed = fi(15 * sin_y_fi, T, Fm);
    
    x_plot = double(x_fixed);
    y_plot = double(y_fixed);
    phase_jumps_x = abs(diff(th_x_float)) > pi;
    phase_jumps_y = abs(diff(th_y_float)) > pi;
    x_plot([false, phase_jumps_x | phase_jumps_y]) = NaN;
    y_plot([false, phase_jumps_x | phase_jumps_y]) = NaN;

    MSE_results(i) = mean((x_ideal - double(x_fixed)).^2 + (y_ideal - double(y_fixed)).^2);
    
    subplot(2, 2, i);
    plot(x_ideal, y_ideal, 'k', 'LineWidth', 1.5); hold on;
    plot(x_plot, y_plot, 'r.-', 'MarkerSize', 5, 'LineWidth', 1);
    title(sprintf('FL = %d (WL = %d) | MSE = %.4f', FL, WL, MSE_results(i)));
    xlabel('X'); ylabel('Y');
    legend('Ideal', 'Maclaurin Fixed-Point', 'Location', 'best');
    grid on; axis equal;
end

figure('Name', 'MSE Trend Analysis', 'Position', [150, 150, 600, 400]);
FL_trend = 1:15;
MSE_trend = zeros(1, length(FL_trend));

for k = 1:length(FL_trend)
    FL_t = FL_trend(k); WL_t = 8 + FL_t;
    T_t = numerictype(1, WL_t, FL_t);
    th_x_t = fi(th_x_float, T_t, Fm); th_y_t = fi(th_y_float, T_t, Fm);
    c_sin_t = fi([1/factorial(9), 1/factorial(7), 1/factorial(5), 1/factorial(3), 1], T_t, Fm);
    x2_t = th_x_t .* th_x_t; y2_t = th_y_t .* th_y_t;
    sx_t = th_x_t .* (c_sin_t(5) - x2_t .* (c_sin_t(4) - x2_t .* (c_sin_t(3) - x2_t .* (c_sin_t(2) - x2_t .* c_sin_t(1)))));
    sy_t = th_y_t .* (c_sin_t(5) - y2_t .* (c_sin_t(4) - y2_t .* (c_sin_t(3) - y2_t .* (c_sin_t(2) - y2_t .* c_sin_t(1)))));
    xf_t = double(fi(15 * sx_t, T_t, Fm)); yf_t = double(fi(15 * sy_t, T_t, Fm));
    MSE_trend(k) = mean((x_ideal - xf_t).^2 + (y_ideal - yf_t).^2);
end

semilogy(FL_trend, MSE_trend, 'b-o', 'LineWidth', 2, 'MarkerFaceColor', 'b');
title('MSE Trend vs. Fraction Length (FL)');
xlabel('Fraction Length (Bits)'); ylabel('Mean Squared Error (MSE) - Log Scale');
grid on;