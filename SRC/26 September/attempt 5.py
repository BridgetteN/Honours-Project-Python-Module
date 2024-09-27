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


def draw(nodes, bezier_curves, width=800, height=600):
    screen = pydraw.Screen(width, height)

    # Draw nodes as circles
    radius = 30  # Maintain the radius as per your original script
    for (node, (x, y)) in nodes.items():
        pydraw.Oval(screen, x - radius // 2, height - (y + radius // 2), radius, radius)

    # Draw Bézier curves
    for x0, y0 in bezier_curves:
        number_of_points = len(x0)
        for i in range(number_of_points - 1):
            pydraw.Line(screen, x0[i], height - y0[i], x0[i + 1], height - y0[i + 1])

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

    # Coordinates for Bézier curve from Node 1 (Glucose) to Node 4 (Glucose-6-phosphate)
    P0 = (100, 500)  # Node 1
    P2 = (300, 400)  # Node 4
    control_x0, control_y0 = (200, 550)  # Control point for the curve
    x0, y0 = calculate_bezier(P0, (control_x0, control_y0), P2, 100)

    # Combine Bézier curves into a list
    bezier_curves = [(x0, y0)]

    # Draw everything
    screen = draw(nodes, bezier_curves)

    screen.listen()
    screen.loop()

