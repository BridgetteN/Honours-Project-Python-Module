from math import sin, cos, radians, sqrt, asin, degrees
import pydraw
import sys

# Define your rotate_point function to rotate vectors
def rotate_point(x1, y1, rotation_angle):
    x2 = x1 * cos(radians(rotation_angle)) - y1 * sin(radians(rotation_angle))
    y2 = x1 * sin(radians(rotation_angle)) + y1 * cos(radians(rotation_angle))
    return x2, y2

# Bezier calculation for a quadratic curve
def calculate_bezier_Q_t(P0, P1, P2, t):
    Q_t = ((1 - t) * (1 - t) * P0) + (2 * t * (1 - t) * P1) + (t * t * P2)
    return Q_t

# Helper function to find the center of four points
def find_centre_of_four_points(P0, P1, P2, P3):
    centre_X_1 = P0[0] + (P1[0] - P0[0]) / 2
    centre_Y_1 = P0[1] + (P1[1] - P0[1]) / 2
    centre_X_2 = P2[0] + (P3[0] - P2[0]) / 2
    centre_Y_2 = P2[1] + (P3[1] - P2[1]) / 2
    centre_X = centre_X_1 + (centre_X_2 - centre_X_1) / 2
    centre_Y = centre_Y_1 + (centre_Y_2 - centre_Y_1) / 2
    return centre_X, centre_Y

# Calculate control points for the curves
def calculate_bezier_series(P0, P1, P2, number_of_steps):
    t = [0]
    coords = []
    for i in range(1, number_of_steps + 1):
        t.append(i / number_of_steps)
    for i in range(len(t)):
        coords.append(calculate_bezier_Q_t(P0, P1, P2, t[i]))
    return coords

# Generate the Bezier curve coordinates
def calculate_bezier(P0, P1, P2, number_of_steps):
    x = calculate_bezier_series(P0[0], P1[0], P2[0], number_of_steps)
    y = calculate_bezier_series(P0[1], P1[1], P2[1], number_of_steps)
    return x, y

# Draw function that utilizes pydraw
def draw(screen, x0, y0, x1, y1, nodes, edges, width=800, height=600, x_scale=50, y_scale=50, x_offset=100, y_offset=100):
    # Draw nodes (metabolites) with labels
    radius = 10
    for node, pos in nodes.items():
        pydraw.Oval(screen, (x_offset + x_scale * pos[0]) - radius / 2,
                    height - (y_offset + y_scale * pos[1] + radius / 2), radius, radius)
        pydraw.Text(screen, node, x_offset + x_scale * pos[0], height - y_offset - y_scale * pos[1] - 15)

    # Draw edges (reactions) connecting nodes
    for edge in edges:
        pydraw.Line(screen, x_scale * nodes[edge[0]][0] + x_offset, height - y_offset - y_scale * nodes[edge[0]][1],
                    x_offset + x_scale * nodes[edge[1]][0], height - y_offset - y_scale * nodes[edge[1]][1])

    # Draw the two Bézier curves
    for i in range(len(x0) - 1):
        pydraw.Line(screen, x_scale * x0[i] + x_offset, height - y_offset - y_scale * y0[i],
                    x_offset + x_scale * x0[i + 1], height - y_offset - y_scale * y0[i + 1])
        pydraw.Line(screen, x_scale * x1[i] + x_offset, height - y_offset - y_scale * y1[i],
                    x_offset + x_scale * x1[i + 1], height - y_offset - y_scale * y1[i + 1])

    screen.update()

    return screen

# Main program that will handle Bézier drawing
if __name__ == '__main__':
    P0 = (0, 0)
    P1 = (2, 3)
    P2 = (4, 0)
    P3 = (6, 2)
    number_of_steps = 10

    # Nodes and edges for metabolic pathways (adjust to your coordinates)
    nodes = {
        'Glucose': (0, 2),
        'G6P': (2, 3),
        'F1,6Bisp': (4, 2),
        'DHAP': (5, 3),
        'GA3P': (6, 1),
        'PYR': (10, 2),
    }

    edges = [
        ('Glucose', 'G6P'),
        ('G6P', 'F1,6Bisp'),
        ('F1,6Bisp', 'DHAP'),
        ('DHAP', 'GA3P'),
        ('GA3P', 'PYR')
    ]

    # Calculate the Bézier curve points for two separate curves
    x0, y0 = calculate_bezier(P0, P1, P2, number_of_steps)
    x1, y1 = calculate_bezier(P1, P2, P3, number_of_steps)

    # Create a pydraw screen
    screen = pydraw.Screen(800, 600)

    # Call the draw function to create the visualization
    screen = draw(screen, x0, y0, x1, y1, nodes, edges)
    screen.listen()  # Listen for events (you can press Esc to close)
    screen.loop()  # Keep the screen running
