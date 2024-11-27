import math

BALL_RADIUS = 0.0127
LENGTH = 0.417
LEN_SMALL = BALL_RADIUS
LEN_BIG = LENGTH - BALL_RADIUS
ANG_SMALL = - math.pi / 4
ANG_BIG = math.pi / 4

v1 = 6.157
x1 = LEN_SMALL
v2 = 5.072
x2 = LEN_BIG

# Define the two points (voltage, gear_angle)
point1 = (v1, x1)
point2 = (v2, x2)

# Calculate the slope (m)
m = (point2[1] - point1[1]) / (point2[0] - point1[0])

# Calculate the y-intercept (b)
b = point1[1] - m * point1[0]

# Display the equation
t = str(input("angle or pos:"))
if t == "angle":
    print(f"The equation for gear angle in terms of voltage is: gear_angle = {m:.4f} * voltage + {b:.4f}")
else:
    print(f"The equation for ball position in terms of voltage is: ball_pos = {m:.4f} * voltage + {b:.4f}")

