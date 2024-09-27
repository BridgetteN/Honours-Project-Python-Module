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


def findcontrol_point_for_intercept(P0, P2, intercept_point):
    X = (intercept_point[0] - 0.25 * P0[0] - 0.25 * P2[0]) / 0.5
    Y = (intercept_point[1] - 0.25 * P0[1] - 0.25 * P2[1]) / 0.5
    return (X, Y)


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
    cx, cy = ((P0[0] + P2[0]) / 2, (P0[1] + P2[1]) / 2)
    control_x0, control_y0 = findcontrol_point_for_intercept(P0, P2, (cx, cy))
    control_x1, control_y1 = findcontrol_point_for_intercept(P1, P3, (cx, cy))
    x0, y0 = calculate_bezier(P0, (control_x0, control_y0), P2, number_of_steps)
    x1, y1 = calculate_bezier(P1, (control_x1, control_y1), P3, number_of_steps)
    return x0, y0, x1, y1


def draw(nodes, bezier_curves, width=800, height=600):
    screen = pydraw.Screen(width, height)

    # Draw nodes as circles
    radius = 30
    for (node, (x, y)) in nodes.items():
        pydraw.Oval(screen, x - radius // 2, height - (y + radius // 2), radius, radius)

    # Draw Bézier curves
    for x0, y0, x1, y1 in bezier_curves:
        number_of_points = len(x0)
        for i in range(number_of_points - 1):
            pydraw.Line(screen, x0[i], height - y0[i], x0[i + 1], height - y0[i + 1])
            pydraw.Line(screen, x1[i], height - y1[i], x1[i + 1], height - y1[i + 1])

    screen.update()
    return screen


def keydown(key):
    print(key)
    if key == 'escape':
        sys.exit()


if __name__ == '__main__':
    # Node coordinates for glycolysis metabolites
    nodes = {
        1: (100, 500),  # Glucose
        2: (150, 450),  # ATP (for Glucose -> Glucose-6-phosphate)
        3: (200, 400),  # ADP (for Glucose -> Glucose-6-phosphate)
        4: (300, 400),  # Glucose-6-phosphate
        5: (500, 300),  # Fructose-6-phosphate
        6: (450, 350),  # ATP (for Fructose-6-phosphate -> G3P/DHAP)
        7: (550, 250),  # ADP (for Fructose-6-phosphate -> G3P/DHAP)
        9: (700, 200),  # G3P/DHAP
    }

    # Bézier curve from Node 1 (Glucose) to Node 4 (Glucose-6-phosphate)
    P0 = (100, 500)  # Node 1
    P2 = (300, 400)  # Node 4
    control_x0, control_y0 = (200, 550)  # Example control point
    x0, y0 = calculate_bezier(P0, (control_x0, control_y0), P2, 100)

    # Bézier curve from Node 2 (ATP) to Node 3 (ADP)
    P1 = (150, 450)  # Node 2
    P3 = (200, 400)  # Node 3
    control_x1, control_y1 = (175, 500)  # Example control point
    x1, y1 = calculate_bezier(P1, (control_x1, control_y1), P3, 100)

    # Combine Bézier curves
    bezier_curves = [(x0, y0, x1, y1)]

    # Draw everything
    screen = draw(nodes, bezier_curves)

    screen.listen()
    screen.loop()
