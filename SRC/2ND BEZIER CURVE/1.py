from math import sin, cos, radians, sqrt, asin, degrees
import pydraw
import sys

def rotate_point(x1, y1, rotation_angle):
    x2 = x1 * cos(radians(rotation_angle)) - y1 * sin(radians(rotation_angle))
    y2 = x1 * sin(radians(rotation_angle)) + y1 * cos(radians(rotation_angle))
    return x2, y2

def calculate_bezier_Q_t(P0, P1, P2, t):
    Q_t = ((1 - t) * (1 - t) * P0) + (2 * t * (1 - t) * P1) + (t * t * P2)
    return Q_t

def find_centre_of_four_points(P0, P1, P2, P3):
    centre_X_1 = P0[0] + (P1[0] - P0[0]) / 2
    centre_Y_1 = P0[1] + (P1[1] - P0[1]) / 2
    centre_X_2 = P2[0] + (P3[0] - P2[0]) / 2
    centre_Y_2 = P2[1] + (P3[1] - P2[1]) / 2
    centre_X = centre_X_1 + (centre_X_2 - centre_X_1) / 2
    centre_Y = centre_Y_1 + (centre_Y_2 - centre_Y_1) / 2
    return centre_X, centre_Y

def findcontrol_point_for_intercept(P0, P2, intercept_point):
    X = (intercept_point[0] - 0.25 * P0[0] - 0.25 * P2[0]) / 0.5
    Y = (intercept_point[1] - 0.25 * P0[1] - 0.25 * P2[1]) / 0.5
    return X, Y

def calculate_control_point(x0, y0, x1, y1, distance):
    r = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    control_point = (r / 2, distance)
    angle = degrees(asin((y1 - y0) / r))
    c0, c1 = rotate_point(control_point[0], control_point[1], angle)
    return c0 + x0, c1 + y0

def calculate_bezier_series(P0, P1, P2, number_of_steps):
    t = [i / number_of_steps for i in range(number_of_steps + 1)]
    return [calculate_bezier_Q_t(P0, P1, P2, ti) for ti in t]

def calculate_bezier(P0, P1, P2, number_of_steps):
    x = calculate_bezier_series(P0[0], P1[0], P2[0], number_of_steps)
    y = calculate_bezier_series(P0[1], P1[1], P2[1], number_of_steps)
    return x, y

def calculate_two_arrow_bezier_with_new_point(P0, P1, P2, P3, P4, P5, number_of_steps):
    # Calculate control points and curves for P0 -> P2, P1 -> P3
    cx, cy = find_centre_of_four_points(P0, P1, P2, P3)
    control_x0, control_y0 = findcontrol_point_for_intercept(P0, P2, (cx, cy))
    control_x1, control_y1 = findcontrol_point_for_intercept(P1, P3, (cx, cy))
    x0, y0 = calculate_bezier(P0, (control_x0, control_y0), P2, number_of_steps)
    x1, y1 = calculate_bezier(P1, (control_x1, control_y1), P3, number_of_steps)

    # Calculate the curve for P3 -> P4
    control_x2, control_y2 = calculate_control_point(P3[0], P3[1], P4[0], P4[1], 0.5)
    x2, y2 = calculate_bezier(P3, (control_x2, control_y2), P4, number_of_steps)

    # Calculate the curve for P4 -> P5 (new curve)
    control_x3, control_y3 = calculate_control_point(P4[0], P4[1], P5[0], P5[1], 0.5)
    x3, y3 = calculate_bezier(P4, (control_x3, control_y3), P5, number_of_steps)

    return x0, y0, x1, y1, x2, y2, x3, y3

def draw_with_new_node(x0, y0, x1, y1, x2, y2, x3, y3, P0, P1, P2, P3, P4, P5, width=800, height=600, x_scale=100, y_scale=100, x_offset=100, y_offset=100, radius=10):
    screen = pydraw.Screen(width, height)

    # Original points
    for P in [P0, P1, P2, P3, P4, P5]:
        pydraw.Oval(screen, (x_offset + x_scale * P[0]) - radius / 2, height - (y_offset + y_scale * P[1]) - radius / 2, radius, radius)

    # Draw the bezier curves
    for points in [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]:
        for i in range(len(points[0]) - 1):
            pydraw.Line(screen, x_scale * points[0][i] + x_offset, height - y_offset - y_scale * points[1][i],
                        x_scale * points[0][i + 1] + x_offset, height - y_offset - y_scale * points[1][i + 1])

    screen.update()
    return screen

if __name__ == '__main__':
    P0 = (0, 0)
    P1 = (2, 0)
    P2 = (0, 3)
    P3 = (2, 2)
    P4 = (4, 4)
    P5 = (6, 5)  # New point to extend the Bézier curve from P4
    number_of_steps = 10

    x0, y0, x1, y1, x2, y2, x3, y3 = calculate_two_arrow_bezier_with_new_point(P0, P1, P2, P3, P4, P5, number_of_steps)
    screen = draw_with_new_node(x0, y0, x1, y1, x2, y2, x3, y3, P0, P1, P2, P3, P4, P5)
    screen.listen()
    screen.loop()
