% Define the PID parameters
Kp = 10.75;
Ti = 3.07;
Td = 1.45;

% Create the parameter vector x as specified
x = [Kp; Ti; Td];

% Call the Q2_perfFCN function
[ISE, t_r, t_s, M_p] = Q2_perfFCN(x);

% Display the results
fprintf('ISE: %.2f\n', ISE);
fprintf('Rise Time (t_r): %.2f s\n', t_r);
fprintf('Settling Time (t_s): %.2f s\n', t_s);
fprintf('Maximum Overshoot (M_p): %.2f%%\n', M_p);