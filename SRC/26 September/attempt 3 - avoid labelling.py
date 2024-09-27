import pydraw
import sys


def draw_glycolysis_diagram():
    width, height = 800, 600
    screen = pydraw.Screen(width, height)

    # Node coordinates
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

    # References for the nodes
    node_references = {
        1: "Glucose",
        2: "ATP for Glucose -> Glucose-6-phosphate",
        3: "ADP for Glucose -> Glucose-6-phosphate",
        4: "Glucose-6-phosphate",
        5: "Fructose-6-phosphate",
        6: "ATP for Fructose-6-phosphate -> G3P/DHAP",
        7: "ADP for Fructose-6-phosphate -> G3P/DHAP",
        9: "Glyceraldehyde-3-phosphate / Dihydroxyacetone phosphate (G3P/DHAP)"
    }

    # Print node references to the console
    for node, description in node_references.items():
        print(f"Node {node}: {description}")

    # Draw the nodes as circles without labeling them
    for node, (x, y) in nodes.items():
        radius = 30
        pydraw.Oval(screen, x - radius // 2, height - (y + radius // 2), radius, radius)

    # Draw the arrows/lines representing the reactions between nodes
    reactions = [
        (1, 2),  # Glucose -> ATP involvement
        (2, 3),  # ATP -> ADP
        (3, 4),  # ADP -> Glucose-6-phosphate
        (4, 5),  # Glucose-6-phosphate -> Fructose-6-phosphate
        (5, 6),  # Fructose-6-phosphate -> ATP involvement
        (6, 7),  # ATP -> ADP
        (7, 9),  # ADP -> G3P/DHAP
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
