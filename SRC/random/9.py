from math import sin, cos, radians, sqrt, asin, degrees
import pydraw
import sys

def rotate_point(x1, y1, rotation_angle):
    """
    This function converts the 2D vector coordinates x1,y1 to a new
    vector x2,y2 by rotating vector x1,y1 by rotation_angle degrees.
    A positive rotation angle is an anti-clockwise rotation
    :param x1: x coordinate of vector
    :param y1: y coordinate of vector
    :param rotation_angle: die rotation angle in degrees. Positive values are anti-clockwise
    :return:
    x2 (float): the x coordinate of the rotated vector
    y2 (float): the y coordinate of the rotated vector
    """
    x2 = x1*cos(radians(rotation_angle))-y1*sin(radians(rotation_angle))
    y2 = x1*sin(radians(rotation_angle))+y1*cos(radians(rotation_angle))
    return x2,y2

def calculate_bezier_Q_t(P0, P1, P2, t):
    """
    This function calculates the x or y value of a quadratic Bezier
    curve give the start (P0), end (P2) and control point (P1) coordinates
    :param P0: the x or y coordinate of the start of the bezier curve
    :param P1: the x or y coordinate of the control point of the Bezier curve
    :param P2: te x or y coordinbate of the end of the Bezier curve
    :param t: the fraction between 0 and 1 (inclusive)
    :return:
    Q_t (float) the x or y coordinate of the Bezier curve at fraction t of its length
    """
    Q_t = ((1-t)*(1-t)*P0) + (2*t*(1-t)*P1) + (t*t*P2)

    return Q_t

def find_centre_of_four_points(P0, P1, P2, P3):
    centre_X_1 = P0[0] + (P1[0]-P0[0])/2
    centre_Y_1 = P0[1] + (P1[1] - P0[1])/2
    centre_X_2 = P2[0] + (P3[0] - P2[0])/2
    centre_Y_2 = P2[1] + (P3[1] - P2[1])/2
    centre_X = centre_X_1 + (centre_X_2 - centre_X_1)/2
    centre_Y = centre_Y_1 + (centre_Y_2 - centre_Y_1)/2
    return (centre_X, centre_Y)

def find_centre_of_four_points(P4, P5, P6, P7):
    centre_X1 = P4[3] + (P5[3]-P4[3])/2
    centre_Y1 = P4[4] + (P5[4] - P4[4])/2
    centre_X2 = P6[3] + (P7[3] - P6[3])/2
    centre_Y2 = P6[4] + (P7[4] - P6[4])/2
    centreX = centre_X1 + (centre_X2 - centre_X1)/2
    centreY = centre_Y1 + (centre_Y2 - centre_Y1)/2
    return (centreX, centreY)


def findcontrol_point_for_intercept(P0, P2, intercept_point):
    X = (intercept_point[0]-0.25*P0[0] - 0.25*P2[0])/0.5
    Y = (intercept_point[1] - 0.25 * P0[1] - 0.25 * P2[1]) / 0.5
    return(X,Y)

def findcontrol_point_for_intercept(P4, P6, intercept_point):
    X = (intercept_point[3]-0.25*P0[3] - 0.25*P2[3])/0.5
    Y = (intercept_point[4] - 0.25 * P0[4] - 0.25 * P2[4]) / 0.5
    return(X,Y)

def calculate_control_point(x0,y0,x1,y1,distance):

    a= ((x1-x0)**2)
    b = ((y1-y0)**2)

    r = sqrt(a + b)
    control_point = (r/2,distance)
    angle = degrees(asin((y1-y0)/r))
    c0, c1 = rotate_point(control_point[0], control_point[1], angle)
    return (c0+x0,c1+y0)



def calculate_bezier_series(P0, P1, P2, number_of_steps):
    t = [0]
    coords = []
    for i in range(1,number_of_steps+1):
       t.append(i/number_of_steps)
    for i in range(len(t)):
       coords.append(calculate_bezier_Q_t(P0, P1, P2, t[i]))
    return coords

def calculate_bezier_series(P4, P5, P6, number_of_steps):
    t1 = [0]
    coords = []
    for i in range(1,number_of_steps+1):
       t1.append(i/number_of_steps)
    for i in range(len(t1)):
       coords.append(calculate_bezier_Q_t(P4, P5, P6, t1[i]))
    return coords

def calculate_bezier(P4, P5, P7, number_of_steps):

    x1_1 = calculate_bezier_series(P4[3], P5[3], P6[3], number_of_steps)
    y1_1 = calculate_bezier_series(P4[4], P5[4], P6[4], number_of_steps)
    return x1_1, y1_1

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

def calculate_two_arrow_bezier(P4, P5, P6, P7, number_of_steps):

    cx1, cy1 = find_centre_of_four_points(P4, P5, P6, P7)
    control1_x0, control1_y0 = findcontrol_point_for_intercept(P4, P6, (cx1, cy1))
    control1_x1, control1_y1 = findcontrol_point_for_intercept(P5, P7, (cx1, cy1))
    x1_0, y1_0 = calculate_bezier(P4, (control1_x0, control1_y0), P6, number_of_steps)
    x1_1, y1_1 = calculate_bezier(P5, (control1_x1, control1_y1), P7, number_of_steps)
    return x1_0, y1_0, x1_1, y1_1

def draw(x0, y0, x1, y1, width=800, height=600, x_scale=100, y_scale=100, x_offset=100, y_offset=100, radius=10):
    screen = pydraw.Screen(width, height)
    pydraw.Oval(screen, (x_offset + x_scale * (P0[0])) - radius / 2,
             height - (y_offset + y_scale * (P0[1]) + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P1[0]) - radius / 2, height - (y_offset + y_scale * P1[1] + radius / 2),
             radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P2[0]) - radius / 2, height - (y_offset + y_scale * P2[1] + radius / 2),
             radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P3[0]) - radius / 2, height - (y_offset + y_scale * P3[1] + radius / 2),
             radius, radius)

    number_of_points = len(x0)
    for i in range(number_of_points - 1):
       pydraw.Line(screen, x_scale * x0[i] + x_offset, height - y_offset - y_scale * y0[i],
                x_offset + x_scale * x0[i + 1], height - y_offset - y_scale * y0[i + 1])
       pydraw.Line(screen, x_scale * x1[i] + x_offset, height - y_offset - y_scale * y1[i],
                x_offset + x_scale * x1[i + 1], height - y_offset - y_scale * y1[i + 1])
    screen.update()

    return screen

def draw(x1_0, y1_0, x1_1, y1_1, width=800, height=600, x_scale=100, y_scale=100, x_offset=100, y_offset=100, radius=10):
    screen = pydraw.Screen(width, height)
    pydraw.Oval(screen, (x_offset + x_scale * (P4[3])) - radius / 2,
             height - (y_offset + y_scale * (P4[4]) + radius / 2), radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P5[3]) - radius / 2, height - (y_offset + y_scale * P5[4] + radius / 2),
             radius, radius)]
    pydraw.Oval(screen, (x_offset + x_scale * P6[3]) - radius / 2, height - (y_offset + y_scale * P6[4] + radius / 2),
             radius, radius)
    pydraw.Oval(screen, (x_offset + x_scale * P7[4]) - radius / 2, height - (y_offset + y_scale * P7[4] + radius / 2),
             radius, radius


number_of_points = len(x1_0)
for i in range(number_of_points - 1):
    pydraw.Line(screen, x_scale * x0[i] + x_offset, height - y_offset - y_scale * y0[i],
                x_offset + x_scale * x0[i + 1], height - y_offset - y_scale * y0[i + 1])
    pydraw.Line(screen, x_scale * x1[i] + x_offset, height - y_offset - y_scale * y1[i],
                x_offset + x_scale * x1[i + 1], height - y_offset - y_scale * y1[i + 1])
screen.update()

return screen


def keydown(key):
    print(key)
    if key == 'escape':
       sys.exit()
    return


if __name__ == '__main__':


    P0 =(0,0)
    P2 = (0, 3)
    P1 = (2, 0)
    P3 = (2, 2)
    number_of_steps = 10

    x0, y0, x1, y1 = calculate_two_arrow_bezier(P0, P1, P2, P3, number_of_steps)
    screen = draw(x0, y0, x1, y1)
    screen.listen()
    screen.loop()
       # for event in pydraw.event.get():
       #  if event.type == pydraw.QUIT:
       #     running = False
       #  if event.type == pydraw.KEYDOWN:
       #     if event.key == pydraw.K_ESCAPE:
       #        running = False
