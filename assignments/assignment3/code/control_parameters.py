import matlab.engine
import numpy as np

def performance_results(kp, ti, td, eng):
    # Have to convert into a 2D list for MATLAB because it's weird
    x_ml = matlab.double([[kp], [ti], [td]])

    ISE, t_r, t_s, M_p = eng.Q2_perfFCN(x_ml, nargout=4)

    if any(map(lambda v: np.isnan(v) or np.isinf(v), [ISE, t_r, t_s, M_p])):
        return float('inf'), float('inf'), float('inf'), float('inf')

    return ISE, t_r, t_s, M_p

# Example usage
# x = [10, 3, 0.5]  # Example input for Kp, Ti, Td
# ISE, t_r, t_s, M_p = performance_results(x[0], x[1], x[2])
# print(f"ISE: {ISE}, Rise Time: {t_r} s, Settling Time: {t_s} s, Maximum Overshoot: {M_p}%")
