import math

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from .combine import Combine

# mouse pointer
lastPosX = 0
lastPosY = 0
zoomScale = 1.0
dataL = 0
xRot = 0
yRot = 0
zRot = 0


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
    increment = 0.30

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # wheel rolled up
        glScaled(1 + increment, 1 + increment, 1 + increment)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # wheel rolled down
        glScaled(1 - increment, 1 - increment, 1 - increment)

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


class STL:
    def __init__(self, obj):
        self.obj = obj
        self.init_shadding()

    def draw(self):
        glBegin(GL_TRIANGLES)
        for vector, normal in zip(self.obj.vectors, self.obj.normals):
            glColor3f(0, 0.3, 0.8)
            glNormal3f(normal[0], normal[1], normal[2])
            glVertex3f(vector[0][0], vector[0][1], vector[0][2])
            glVertex3f(vector[1][0], vector[1][1], vector[1][2])
            glVertex3f(vector[2][0], vector[2][1], vector[2][2])
        glEnd()

    def init_shadding(self):
        # solid model with a light / shading
        glShadeModel(GL_SMOOTH)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        # glLight(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))
        glLight(GL_LIGHT0, GL_POSITION,  (0, 0, 1, 0))  # directional light from the front
        glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))  # point light from the left, top, front
        glLight(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glMatrixMode(GL_MODELVIEW)


def render_2d(window, model, filename):
    # render 2d images
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    model()
    pygame.image.save(window, filename)
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    display = (1920, 1080)
    window = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (1.0 * display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -20)
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)
    # stl = STL("USP9.stl")
    file1 = "./samples/handgun.stl"
    file2 = "./samples/door_handle.stl"
    file3 = "./samples/mouse.stl"
    file4 = "./samples/knife.stl"
    com = Combine([file1, file2, file3])
    combined_object = com.combine()
    stl = STL(combined_object)

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
        stl.draw()
        pygame.display.flip()
        # pygame.time.wait(1)
