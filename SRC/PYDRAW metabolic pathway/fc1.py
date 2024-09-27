import numpy as np
from math import sin, cos, radians



# Define your rotate_point function to rotate vectors
def rotate_point(x1, y1, rotation_angle):
    x2 = x1 * cos(radians(rotation_angle)) - y1 * sin(radians(rotation_angle))
    y2 = x1 * sin(radians(rotation_angle)) + y1 * cos(radians(rotation_angle))
    return x2, y2


# Bézier calculation for a quadratic curve
def calculate_bezier_Q_t(P0, P1, P2, t):
    Q_x = ((1 - t) ** 2) * P0[0] + 2 * (1 - t) * t * P1[0] + (t ** 2) * P2[0]
    Q_y = ((1 - t) ** 2) * P0[1] + 2 * (1 - t) * t * P1[1] + (t ** 2) * P2[1]
    return Q_x, Q_y


# Generate the Bézier curve coordinates
def calculate_bezier(P0, P1, P2, number_of_steps):
    t_values = [i / number_of_steps for i in range(number_of_steps + 1)]
    bezier_coords = [calculate_bezier_Q_t(P0, P1, P2, t) for t in t_values]

    x_coords = [coord[0] for coord in bezier_coords]
    y_coords = [coord[1] for coord in bezier_coords]
    return x_coords, y_coords


# Draw function that utilizes pydraw
def draw(screen, bezier_x0, bezier_y0, bezier_x1, bezier_y1, nodes, edges, width=800, height=600, x_scale=50,
         y_scale=50, x_offset=100, y_offset=100):
    # Draw nodes (metabolites) with labels
    radius = 10
    for node, pos in nodes.items():
        # Convert NumPy float64 to Python float
        x_pos = float(pos[0])
        y_pos = float(pos[1])
        # Draw node as an oval
        pydraw.Oval(screen, (x_offset + x_scale * x_pos) - radius / 2,
                    height - (y_offset + y_scale * y_pos + radius / 2), radius, radius)
        # Draw text label for the node
        pydraw.Text(screen, node, x_offset + x_scale * x_pos, height - y_offset - y_scale * y_pos - 15)

    # Draw edges (reactions) connecting nodes
    for edge in edges:
        node1, node2 = edge[0], edge[1]
        x1, y1 = float(nodes[node1][0]), float(nodes[node1][1])
        x2, y2 = float(nodes[node2][0]), float(nodes[node2][1])

        # Ensure the lines touch the node's center
        pydraw.Line(screen, x_scale * x1 + x_offset, height - y_offset - y_scale * y1,
                    x_scale * x2 + x_offset, height - y_offset - y_scale * y2)

    # Draw the two Bézier curves
    print("Drawing Bézier curves...")
    print(f"bezier_x0: {bezier_x0}")
    print(f"bezier_y0: {bezier_y0}")
    print(f"bezier_x1: {bezier_x1}")
    print(f"bezier_y1: {bezier_y1}")

    for i in range(len(bezier_x0) - 1):
        pydraw.Line(screen, x_scale * bezier_x0[i] + x_offset, height - y_offset - y_scale * bezier_y0[i],
                    x_scale * bezier_x0[i + 1] + x_offset, height - y_offset - y_scale * bezier_y0[i + 1])
        pydraw.Line(screen, x_scale * bezier_x1[i] + x_offset, height - y_offset - y_scale * bezier_y1[i],
                    x_scale * bezier_x1[i + 1] + x_offset, height - y_offset - y_scale * bezier_y1[i + 1])

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
        'hexokinase': np.array([0, 1]),
        '.': np.array([2, 1]),
        'G6P': np.array([2, 2]),
        'F6P': np.array([3, 2]),
        'F1,6Bisp': np.array([5, 2]),
        'DHAP': np.array([6, 3]),
        'Ga3P': np.array([6, 1]),
        'GA3P': np.array([8, 3]),
        '1,3BG': np.array([8, 1]),
        'PGK': np.array([9, 0]),
        '2,3BG': np.array([9, 2]),
        '2PG': np.array([10, 0]),
        'PPP': np.array([11, 0]),
        'Glucose': np.array([0, 2]),
        'ATP': np.array([0, 0]),
        'ADP': np.array([2, 0]),
        'ATP1': np.array([3, 3]),
        'ADP1': np.array([5, 3]),
        'NAD+': np.array([6, 0]),
        'NADH': np.array([8, 0]),
        'ADP2': np.array([11, -2]),
        'ATP2': np.array([13, -2]),
        'PYR': np.array([13, 0])
    }

    edges = [
        ('hexokinase', '.'),
        ('G6P', 'F6P'),
        ('F1,6Bisp', 'DHAP'),
        ('F1,6Bisp', 'Ga3P'),
        ('DHAP', 'GA3P'),
        ('1,3BG', 'PGK'),
        ('1,3BG', '2,3BG'),
        ('PGK', '2PG'),
        ('2PG', 'PPP')
    ]

    # Calculate the Bézier curve points for two separate curves
    bezier_x0, bezier_y0 = calculate_bezier(P0, P1, P2, number_of_steps)
    bezier_x1, bezier_y1 = calculate_bezier(P1, P2, P3, number_of_steps)

    # Create a pydraw screen
    screen = pydraw.Screen(800, 600)

    # Call the draw function to create the visualization
    screen = draw(screen, bezier_x0, bezier_y0, bezier_x1, bezier_y1, nodes, edges)
    screen.listen()  # Listen for events (you can press Esc to close)
    screen.loop()  # Keep the screen running

