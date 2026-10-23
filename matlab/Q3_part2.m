% =========================================================
% Digital Signal Processing - FIR Filter Coefficient Quantization
% =========================================================

clear; clc; close all;

% ۱. تعریف فیلتر و سیگنال ورودی
h = [0.05, -0.1, 0.25, -0.4, 0.6, -0.75, 1.0, -0.75, 0.6, -0.4, 0.25, -0.1, 0.05];
N = 500;
x = randn(1, N); % سیگنال تصادفی با توزیع نرمال (گوسی)

% ۲. محاسبه خروجی ایده‌آل (ممیز شناور)
y_float = conv(x, h);

% ۳. تنظیمات مربوط به فرمت‌های ممیز ثابت
fractional_bits = 8:15; % از Q16.8 تا Q16.15
word_length = 16;       % طول کلمه ثابت 16 بیت

% آماده‌سازی آرایه‌ها برای ذخیره مقادیر خطا
MSE_manual = zeros(1, length(fractional_bits));
SSE_manual = zeros(1, length(fractional_bits));
MSE_tool   = zeros(1, length(fractional_bits));
SSE_tool   = zeros(1, length(fractional_bits));

% آماده‌سازی پنجره رسم نمودارها
figure('Name', 'FFT of Floating vs Fixed-Point FIR', 'Position', [100, 50, 1200, 900]);

fprintf('========================================================================\n');
fprintf(' Format  |  MSE (Manual)  |  SSE (Manual)  |   MSE (Tool)   |   SSE (Tool)\n');
fprintf('========================================================================\n');

% حلقه تکرار برای تست تمامی فرمت‌های خواسته شده
for i = 1:length(fractional_bits)
    f = fractional_bits(i);
    
    %% -------- روش دستی (Manual Method) --------
    scale_factor = 2^f;
    h_scaled = round(h * scale_factor);
    
    % اعمال اشباع (Saturation) برای حافظه 16 بیتی علامت‌دار
    max_val = 2^(word_length - 1) - 1; % 32767
    min_val = -2^(word_length - 1);    % -32768
    h_scaled(h_scaled > max_val) = max_val;
    h_scaled(h_scaled < min_val) = min_val;
    
    h_manual = h_scaled / scale_factor;
    y_manual = conv(x, h_manual);
    
    % محاسبه خطاهای روش دستی
    MSE_manual(i) = mean((y_float - y_manual).^2);
    SSE_manual(i) = sum((y_float - y_manual).^2);
    
    %% -------- روش ابزار متلب (Fixed-Point Toolbox) --------
    % تابع fi به طور خودکار عملیات گرد کردن و اشباع را انجام می‌دهد
    h_tool_obj = fi(h, 1, word_length, f);
    h_tool = double(h_tool_obj);
    y_tool = conv(x, h_tool);
    
    % محاسبه خطاهای ابزار
    MSE_tool(i) = mean((y_float - y_tool).^2);
    SSE_tool(i) = sum((y_float - y_tool).^2);
    
    % چاپ نتایج در کنسول
    fprintf(' Q16.%-2d  |   %1.4e  |   %1.4e  |   %1.4e  |   %1.4e \n', ...
        f, MSE_manual(i), SSE_manual(i), MSE_tool(i), SSE_tool(i));
    
    %% -------- محاسبه و رسم FFT --------
    N_fft = 1024;
    Y_float_fft = 20*log10(abs(fft(y_float, N_fft)));
    Y_manual_fft = 20*log10(abs(fft(y_manual, N_fft)));
    
    freq_axis = linspace(0, 1, N_fft/2);
    
    subplot(4, 2, i);
    plot(freq_axis, Y_float_fft(1:N_fft/2), 'b', 'LineWidth', 1.5); hold on;
    plot(freq_axis, Y_manual_fft(1:N_fft/2), 'r--', 'LineWidth', 1.2);
    title(sprintf('Format: Q16.%d', f));
    if i >= 7
        xlabel('Normalized Frequency (\times \pi rad/sample)');
    end
    ylabel('Magnitude (dB)');
    grid on;
    
    if i == 1
        legend('Floating-Point (Ideal)', 'Fixed-Point');
    end
end
fprintf('========================================================================\n');