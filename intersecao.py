from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

##List of all created lines.
lines = []

##Class that keeps the coordinates of a point on screen.
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

##Iterate through all lines to find intersections between them.
def findIntersections():
    for i in xrange (0, len(lines)):
        for j in xrange (i + 1, len(lines)):
            p = point(lines[i][0].x, lines[i][0].y)
            q = point(lines[i][1].x, lines[i][1].y)
            r = point(lines[j][0].x, lines[j][0].y)
            s = point(lines[j][1].x, lines[j][1].y)
            getIntersection(p, q, r, s)

##Gets the intersection point of two finite line segments 'pq' and 'rs'.
#Handles division by zero.
#@param p, q First Line Points.
#@param r, s Second Line Points.
def getIntersection(p, q, r, s):
    s1_x = q.x - p.x     
    s1_y = q.y - p.y
    s2_x = s.x - r.x     
    s2_y = s.y - r.y
    s3_x = p.x - r.x
    s3_y = p.y - r.y

    if (-s2_x * s1_y + s1_x * s2_y) == 0:
        return

    s = (-s1_y * s3_x + s1_x * s3_y) / (-s2_x * s1_y + s1_x * s2_y)
    t = ( s2_x * s3_y - s2_y * s3_x) / (-s2_x * s1_y + s1_x * s2_y)

    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        x= p.x + (t * s1_x)
        y = p.y + (t * s1_y)
        p = point(x, y)
        drawPoint(p)

##Convert from mouse coordinates to Ortho2D coordinates.
#@param c Coordinate to be converted.
def convertCoords(c):
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    x = c.x/(width)
    y = c.y/(-height) +1

    return point(x, y)

##Redraw all lines form 'lines' list.
#All lines must be redraw every time display callback is called.
def redrawLines():
    for line in lines:
        drawLine(line[0], line[1])

##Draws a point on screen based on a given coordinate.
#@param c Point we want to draw.
def drawPoint(c):
    glEnable(GL_POINT_SMOOTH)
    glColor3f(0.2, 1.0, 0.2)
    glPointSize(15.0)    

    glBegin(GL_POINTS)
    glVertex2f(c.x, c.y)
    glEnd()

##Draws a line segment on screen based on two given coordinates.
#@param c1 First point of the line segment.
#@param c2 Second point of the line segment.
def drawLine(c1, c2):
    glColor3f(1.0, 0.5, 0.8)
    glLineWidth(1.5)    

    glBegin(GL_LINES)
    glVertex2f(c1.x, c1.y)
    glVertex2f(c2.x, c2.y)
    glEnd()

line_start = point(0, 0)
##Mouse callback function
#Checks if mouse left button was pressed.
#Creates a line with mouse coordinates when left button is released.
#@param button Pressed button.
#@param state State of the button.
#@param x X coord of mouse.
#@param y Y coord of mouse.
def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        global line_start        
        if state == GLUT_DOWN:
            line_start = convertCoords(point(x, y))

        elif state == GLUT_UP:
            line_end = convertCoords(point(x, y))
            lines.append([line_start, line_end])

##Display callback function
def display():
    glClearColor(0.1, 0.1, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    redrawLines()
    findIntersections()

    glutSwapBuffers()

##Reshape callback function
def reshape(w, h):
    glViewport (0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)

##Main
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(400, 400)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("intersection")
glutDisplayFunc(display)
glutIdleFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMainLoop()
