from math import sin, cos, radians, sqrt, asin, degrees
import pydraw


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
    return (X, Y)


def calculate_control_point(x0, y0, x1, y1, distance):
    a = ((x1 - x0) ** 2)
    b = ((y1 - y0) ** 2)
    r = sqrt(a + b)
    control_point = (r / 2, distance)
    angle = degrees(asin((y1 - y0) / r))
    c0, c1 = rotate_point(control_point[0], control_point[1], angle)
    return (c0 + x0, c1 + y0)


def calculate_bezier_series(P0, P1, P2, number_of_steps):
    t = [0]
    coords = []
    for i in range(1, number_of_steps + 1):
        t.append(i / number_of_steps)
    for i in range(len(t)):
        coords.append(calculate_bezier_Q_t(P0, P1, P2, t[i]))
    return coords


def calculate_bezier(P0, P1, P2, number_of_steps):
    x = calculate_bezier_series(P0[0], P1[0], P2[0], number_of_steps)
    y = calculate_bezier_series(P0[1], P1[1], P2[1], number_of_steps)
    return x, y


def calculate_two_arrow_bezier(P0, P1, P2, P3, number_of_steps):
    cx, cy = find_centre_of_four_points(P0, P1, P2, P3)
    control_x0, control_y0 = findcontrol_point_for_intercept(P0, P2, (cx, cy))
    control_x1, control_y1 = findcontrol_point_for_intercept(P1, P3, (cx, cy))
    x0, y0 = calculate_bezier(P0, (control_x0, control_y0), P2, number_of_steps)
    x1, y1 = calculate_bezier(P1, (control_x1, control_y1), P3, number_of_steps)
    return x0, y0, x1, y1


def draw(x0, y0, x1, y1, x2, y2, P0, P1, P2, P3, P4, P5, width=800, height=600, x_scale=100, y_scale=100, x_offset=100,
         y_offset=100, radius=10):
    screen = pydraw.Screen(width, height)

    # Original points
    pydraw.Oval(screen, (x_offset + x_scale * P0[0]) - radius / 2,
                height - (y_offset + y_scale * P0[1] + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P1[0]) - radius / 2,
                height - (y_offset + y_scale * P1[1] + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P2[0]) - radius / 2,
                height - (y_offset + y_scale * P2[1] + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P3[0]) - radius / 2,
                height - (y_offset + y_scale * P3[1] + radius / 2), radius, radius)

    # New points P4 and P5
    pydraw.Oval(screen, (x_offset + x_scale * P4[0]) - radius / 2,
                height - (y_offset + y_scale * P4[1] + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P5[0]) - radius / 2,
                height - (y_offset + y_scale * P5[1] + radius / 2), radius, radius)

    # Draw bezier curves
    number_of_points = len(x0)
    for i in range(number_of_points - 1):
        pydraw.Line(screen, x_scale * x0[i] + x_offset, height - y_offset - y_scale * y0[i],
                    x_offset + x_scale * x0[i + 1], height - y_offset - y_scale * y0[i + 1])
        pydraw.Line(screen, x_scale * x1[i] + x_offset, height - y_offset - y_scale * y1[i],
                    x_offset + x_scale * x1[i + 1], height - y_offset - y_scale * y1[i + 1])

    # Keep the edge P4 to P2
    pydraw.Line(screen, x_offset + x_scale * P4[0], height - y_offset - y_scale * P4[1],
                x_offset + x_scale * P2[0], height - y_offset - y_scale * P2[1])

    # Draw bezier curve from P4 to P5
    control_x, control_y = calculate_control_point(P4[0], P4[1], P5[0], P5[1], 1)  # Adjust distance as needed
    x4, y4 = calculate_bezier(P4, (control_x, control_y), P5, number_of_steps)
    for i in range(len(x4) - 1):
        pydraw.Line(screen, x_scale * x4[i] + x_offset, height - y_offset - y_scale * y4[i],
                    x_offset + x_scale * x4[i + 1], height - y_offset - y_scale * y4[i + 1])

    screen.update()
    return screen


if __name__ == '__main__':
    P0 = (0, 0)
    P1 = (2, 0)
    P2 = (0, 3)
    P3 = (2, 2)

    # New points P4 and P5
    P4 = (4, 0)
    P5 = (6, 2)

    number_of_steps = 10

    x0, y0, x1, y1 = calculate_two_arrow_bezier(P0, P1, P2, P3, number_of_steps)
    screen = draw(x0, y0, x1, y1, [], [], P0, P1, P2, P3, P4, P5)
    screen.listen()
    screen.loop()

