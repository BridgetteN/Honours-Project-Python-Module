import pydraw
import sys


def draw_glycolysis_diagram():
    width, height = 800, 600
    screen = pydraw.Screen(width, height)

    # Node coordinates (these values are arbitrary and can be adjusted for better layout)
    nodes = {
        1: (100, 500),  # Glucose
        4: (300, 400),  # Glucose-6-phosphate
        5: (500, 300),  # Fructose-6-phosphate
        9: (700, 200),  # Glyceraldehyde-3-phosphate / DHAP
    }

    # Define node names
    node_labels = {
        1: "Glucose (Node 1)",
        4: "Glucose-6-phosphate (Node 4)",
        5: "Fructose-6-phosphate (Node 5)",
        9: "G3P/DHAP (Node 9)",
    }

    # Draw the nodes as circles and label them
    for node, (x, y) in nodes.items():
        radius = 30
        pydraw.Oval(screen, x - radius // 2, height - (y + radius // 2), radius, radius)
        pydraw.Text(screen, node_labels[node], x - 40, height - (y + 50))  # Removed 'fontsize'

    # Draw the arrows/lines representing the reactions between nodes
    reactions = [
        (1, 4),  # Glucose -> Glucose-6-phosphate
        (4, 5),  # Glucose-6-phosphate -> Fructose-6-phosphate
        (5, 9),  # Fructose-6-phosphate -> G3P/DHAP
    ]

    for start, end in reactions:
        x0, y0 = nodes[start]
        x1, y1 = nodes[end]
        pydraw.Line(screen, x0, height - y0, x1, height - y1)

    # Update and display the screen
    screen.update()

    return screen


def keydown(key):
    print(key)
    if key == 'escape':
        sys.exit()


if __name__ == '__main__':
    screen = draw_glycolysis_diagram()
    screen.listen()
    screen.loop()
