from math import sin, cos, radians, sqrt, asin, degrees
import pydraw


def rotate_point(x1, y1, rotation_angle):
    x2 = x1 * cos(radians(rotation_angle)) - y1 * sin(radians(rotation_angle))
    y2 = x1 * sin(radians(rotation_angle)) + y1 * cos(radians(rotation_angle))
    return x2, y2


def calculate_bezier_Q_t(P0, P1, P2, t):
    Q_t_x = ((1 - t) ** 2 * P0[0]) + (2 * t * (1 - t) * P1[0]) + (t ** 2 * P2[0])
    Q_t_y = ((1 - t) ** 2 * P0[1]) + (2 * t * (1 - t) * P1[1]) + (t ** 2 * P2[1])
    return Q_t_x, Q_t_y


def calculate_bezier_series(P0, P1, P2, number_of_steps):
    t = [i / number_of_steps for i in range(number_of_steps + 1)]
    return [calculate_bezier_Q_t(P0, P1, P2, t_val) for t_val in t]


def find_centre_of_four_points(P0, P1, P2, P3):
    centre_X_1 = P0[0] + (P1[0] - P0[0]) / 2
    centre_Y_1 = P0[1] + (P1[1] - P0[1]) / 2
    centre_X_2 = P2[0] + (P3[0] - P2[0]) / 2
    centre_Y_2 = P2[1] + (P3[1] - P2[1]) / 2
    centre_X = centre_X_1 + (centre_X_2 - centre_X_1) / 2
    centre_Y = centre_Y_1 + (centre_Y_2 - centre_Y_1) / 2
    return centre_X, centre_Y


def find_control_point_for_intercept(P0, P2, intercept_point):
    X = (intercept_point[0] - 0.25 * P0[0] - 0.25 * P2[0]) / 0.5
    Y = (intercept_point[1] - 0.25 * P0[1] - 0.25 * P2[1]) / 0.5
    return X, Y


def calculate_two_arrow_bezier(P0, P1, P2, P3, number_of_steps):
    cx, cy = find_centre_of_four_points(P0, P1, P2, P3)
    control_x0, control_y0 = find_control_point_for_intercept(P0, P2, (cx, cy))
    control_x1, control_y1 = find_control_point_for_intercept(P1, P3, (cx, cy))

    x0, y0 = calculate_bezier_series(P0, (control_x0, control_y0), P2, number_of_steps)
    x1, y1 = calculate_bezier_series(P1, (control_x1, control_y1), P3, number_of_steps)
    return x0, y0, x1, y1


def draw(P0, P1, P2, P3, P4, P5, P6, P7, number_of_steps):
    x0, y0, x1, y1 = calculate_two_arrow_bezier(P0, P1, P2, P3, number_of_steps)
    x4, y4, x5, y5 = calculate_two_arrow_bezier(P4, P5, P6, P7, number_of_steps)

    screen = pydraw.Screen(width=800, height=600)

    # Draw points for the first bezier curve
    for point in [P0, P1, P2, P3]:
        pydraw.Oval(screen, (point[0] * 100 + 100) - 5,
                    (600 - (point[1] * 100 + 100)) - 5, 10, 10)

    # Draw points for the second bezier curve
    for point in [P4, P5, P6, P7]:
        pydraw.Oval(screen, (point[0] * 100 + 100) - 5,
                    (600 - (point[1] * 100 + 100)) - 5, 10, 10)

    # Draw bezier curves for both sets of points
    for i in range(len(x0) - 1):
        pydraw.Line(screen, x0[i] * 100 + 100, 600 - (y0[i] * 100 + 100),
                    x0[i + 1] * 100 + 100, 600 - (y0[i + 1] * 100 + 100))
        pydraw.Line(screen, x1[i] * 100 + 100, 600 - (y1[i] * 100 + 100),
                    x1[i + 1] * 100 + 100, 600 - (y1[i + 1] * 100 + 100))

    for i in range(len(x4) - 1):
        pydraw.Line(screen, x4[i] * 100 + 100, 600 - (y4[i] * 100 + 100),
                    x4[i + 1] * 100 + 100, 600 - (y4[i + 1] * 100 + 100))
        pydraw.Line(screen, x5[i] * 100 + 100, 600 - (y5[i] * 100 + 100),
                    x5[i + 1] * 100 + 100, 600 - (y5[i + 1] * 100 + 100))

    screen.update()
    return screen


# Example usage
P0 = (0, 0)
P1 = (1, 2)
P2 = (2, 2)
P3 = (3, 0)
P4 = (0, 1)
P5 = (1, 3)
P6 = (2, 3)
P7 = (3, 1)
number_of_steps = 100

draw(P0, P1, P2, P3, P4, P5, P6, P7, number_of_steps)
