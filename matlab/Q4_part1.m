clear; clc; close all;

W = 32;
F = 24;
T = numerictype(1, W, F);

Fm = fimath('RoundingMethod', 'Floor', ...
            'OverflowAction', 'Wrap', ...
            'SumMode', 'SpecifyPrecision', 'SumWordLength', W, 'SumFractionLength', F, ...
            'ProductMode', 'SpecifyPrecision', 'ProductWordLength', W, 'ProductFractionLength', F);

x_float = linspace(-pi, pi, 1000);
x = fi(x_float, T, Fm);

c_sin = fi([1/factorial(9), 1/factorial(7), 1/factorial(5), 1/factorial(3), 1], T, Fm);
c_cos = fi([1/factorial(8), 1/factorial(6), 1/factorial(4), 1/factorial(2), 1], T, Fm);

x2 = x .* x;

sin_approx = x .* (c_sin(5) - x2 .* (c_sin(4) - x2 .* (c_sin(3) - x2 .* (c_sin(2) - x2 .* c_sin(1)))));
cos_approx = c_cos(5) - x2 .* (c_cos(4) - x2 .* (c_cos(3) - x2 .* (c_cos(2) - x2 .* c_cos(1))));

sin_actual = sin(x_float);
cos_actual = cos(x_float);

error_sin = double(sin_approx) - sin_actual;
error_cos = double(cos_approx) - cos_actual;

mse_sin = mean(error_sin.^2);
max_err_sin = max(abs(error_sin));

mse_cos = mean(error_cos.^2);
max_err_cos = max(abs(error_cos));

fprintf('--- بررسی خطای تقریب ---\n');
fprintf('Sin -> MSE: %e | Max Error: %e\n', mse_sin, max_err_sin);
fprintf('Cos -> MSE: %e | Max Error: %e\n', mse_cos, max_err_cos);

figure('Name', 'Maclaurin Approximation vs Standard MATLAB', 'Position', [100, 100, 1000, 600]);

subplot(2, 2, 1);
plot(x_float, sin_actual, 'b', 'LineWidth', 2); hold on;
plot(x_float, double(sin_approx), 'r--', 'LineWidth', 1.5);
title('Sin(x): MATLAB vs Fixed-Point Maclaurin');
xlabel('x (radians)'); ylabel('sin(x)');
legend('Standard MATLAB', 'Fixed-Point Approximation');
grid on;

subplot(2, 2, 2);
plot(x_float, cos_actual, 'b', 'LineWidth', 2); hold on;
plot(x_float, double(cos_approx), 'r--', 'LineWidth', 1.5);
title('Cos(x): MATLAB vs Fixed-Point Maclaurin');
xlabel('x (radians)'); ylabel('cos(x)');
legend('Standard MATLAB', 'Fixed-Point Approximation');
grid on;

subplot(2, 2, 3);
plot(x_float, error_sin, 'k', 'LineWidth', 1.2);
title(['Error in Sin(x) | Max Err: ', num2str(max_err_sin, '%.4e')]);
xlabel('x (radians)'); ylabel('Amplitude Error');
grid on;

subplot(2, 2, 4);
plot(x_float, error_cos, 'k', 'LineWidth', 1.2);
title(['Error in Cos(x) | Max Err: ', num2str(max_err_cos, '%.4e')]);
xlabel('x (radians)'); ylabel('Amplitude Error');
grid on;