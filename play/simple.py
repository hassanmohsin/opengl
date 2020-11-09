import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

# cubes
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
)

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1)
)

# mouse pointer
lastPosX = 0
lastPosY = 0
zoomScale = 1.0
dataL = 0
xRot = 0
yRot = 0
zRot = 0


def cubes():
    vertices_2 = tuple(tuple(i + 3 for i in v) for v in vertices)
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])

    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices_2[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_2[vertex])
    glEnd()


def cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def key_press(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            glTranslatef(-1, 0, 0)
        if event.key == pygame.K_RIGHT:
            glTranslatef(1, 0, 0)
        if event.key == pygame.K_UP:
            glTranslatef(0, 1, 0)
        if event.key == pygame.K_DOWN:
            glTranslatef(0, -1, 0)
        if event.key == pygame.K_LSHIFT and event.key == pygame.K_UP:
            glRotatef(10, 1, 0, 0)


def mouse_move(event):
    global lastPosX, lastPosY, zoomScale, xRot, yRot, zRot

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # wheel rolled up
        glScaled(1.05, 1.05, 1.05)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # wheel rolled down
        glScaled(0.95, 0.95, 0.95)

    if event.type == pygame.MOUSEMOTION:
        x, y = event.pos
        dx = x - lastPosX
        dy = y - lastPosY

        mouse_state = pygame.mouse.get_pressed()
        if mouse_state[0]:
            model_view = (GLfloat * 16)()
            mvm = glGetFloatv(GL_MODELVIEW_MATRIX, model_view)

            # To combine x-axis and y-axis rotation
            temp = (GLfloat * 3)();
            temp[0] = model_view[0] * dy + model_view[1] * dx
            temp[1] = model_view[4] * dy + model_view[5] * dx
            temp[2] = model_view[8] * dy + model_view[9] * dx
            norm_xy = math.sqrt(temp[0] * temp[0] + temp[1] * temp[1] + temp[2] * temp[2])
            glRotatef(math.sqrt(dx * dx + dy * dy), temp[0] / norm_xy, temp[1] / norm_xy, temp[2] / norm_xy)

        lastPosX, lastPosY = x, y


def render_2d(window, model, filename):
    # render 2d images
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    model()
    pygame.image.save(window, filename)
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    display = (1080, 720)
    window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(60, (1.0 * display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -50)

    # Take care of the hidden surface
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)

    # Take care of the hidden surface
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)

    render_2d(window, cubes, '../images/test0.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == K_ESCAPE:
                pygame.quit()
                quit()

            # Keyboard events
            key_press(event)
            # Mouse events
            mouse_move(event)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cubes()
        pygame.display.flip()
        pygame.time.wait(1)
