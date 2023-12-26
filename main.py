from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time

# Class definition for a moving car
class Car:
    def __init__(self, x, y, z, speed, radius):
        # Initialize car parameters
        self._x = x
        self._y = y
        self._z = z
        self._speed = speed
        self._angle = 0.0  # Initial angle
        self._radius = radius

    def move(self):
        # Move the car along a circular path
        self._angle += self._speed

        # Calculate new position based on the circular path
        self._x = self._radius * math.cos(math.radians(self._angle))
        self._z = self._radius * math.sin(math.radians(self._angle))

    def draw(self):
        # Draw the car using OpenGL commands
        glPushMatrix()
        glTranslatef(self._x, self._y, self._z)

        # Car body
        glPushMatrix()
        glScalef(2, 1, 1)
        glutSolidCube(1)
        glPopMatrix()

        # Front Window
        glColor3f(0.8, 0.8, 0.8)
        glPushMatrix()
        glTranslatef(0, 0.4, 0.5)
        glScalef(0.8, 0.6, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        # Side Windows (Left and Right)
        for x_mul in [-1, 1]:
            glPushMatrix()
            glTranslatef(0.5 * x_mul, 0.4, 0)
            glScalef(0.8, 0.6, 0.1)
            glutSolidCube(1)
            glPopMatrix()

        # Wheels
        glColor3f(0.2, 0.2, 0.2)
        for z_mul in [-1, 1]:
            glPushMatrix()
            glTranslatef(0, -0.3, 0.15 * z_mul)

            for x_mul in [-1, 1]:
                glPushMatrix()
                glTranslatef(0.4 * x_mul, -0.25, 0.4 * z_mul)
                glutSolidTorus(0.05, 0.1, 8, 8)
                glPopMatrix()

            glPopMatrix()

        glPopMatrix()

# Create an instance of the Car class for the moving car
car = Car(x=0, y=(0.5 + 0.1) / 2, z=2.5, speed=2.4, radius=4.0)

# Class definition for a stationary car (subclass of Car)
class StationaryCar(Car):
    def __init__(self, x, y, z, radius):
        # Initialize the stationary car with zero speed
        super().__init__(x, y, z, speed=0, radius=radius)

# Create an instance of the StationaryCar class for the stationary car
stationary_car = StationaryCar(x=-8, y=(0.5 + 0.1) / 2, z=2.5, radius=4.0)

# Function to draw the stationary car
def drawStationaryCar():
    # Set material properties and draw the stationary car
    carMaterial()
    stationary_car.draw()

# Class definition for the camera
class Camera:
    def __init__(self, center, up, min_distance, max_distance, distance=None, angle=0.0):
        self._distance = distance if distance is not None else (max_distance + min_distance) / 2
        self._center = center
        self._up = up
        self._angle = angle
        self._max_distance = max_distance
        self._min_distance = min_distance

    def lookat(self, point):
        x, y, z = self._center
        x += self._distance * math.sin(self._angle)
        z += self._distance * math.cos(self._angle)

        gluLookAt(x, y, z, *point, *self._up)

    def rotate(self, d_angle):
        self._angle += d_angle

    def move(self, distance_change):
        new_distance = self._distance

        new_distance += distance_change

        self._distance = max(min(new_distance, self._max_distance), self._min_distance)

# Create an instance of the Camera class
camera = Camera(
    center=(0, 5, 0),
    up=(0, 1, 0),
    min_distance=3, max_distance=15,
    angle=(math.pi / 4)
)

# Class definition for light sources
class Light:
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular):
        self._intensity_ambient = intensity_ambient
        self._intensity_diffuse = intensity_diffuse
        self._intensity_specular = intensity_specular

    def _setup(self, position, id):
        glLightfv(id, GL_AMBIENT, GLfloat_4(*self._intensity_ambient))
        glLightfv(id, GL_DIFFUSE, GLfloat_4(*self._intensity_diffuse))
        glLightfv(id, GL_SPECULAR, GLfloat_4(*self._intensity_specular))
        glLightfv(id, GL_POSITION, GLfloat_4(*position))

        glEnable(id)

# Class definition for a positioned light (subclass of Light)
class PositionedLight(Light):
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular, position):
        super().__init__(intensity_ambient, intensity_diffuse, intensity_specular)
        self._position = position

    def setup(self, id):
        # Set up the positioned light in the scene
        self._setup(self._position, id)

# Class definition for a rotating light (subclass of Light)
class RotatingLight(Light):
    def __init__(self, intensity_ambient, intensity_diffuse, intensity_specular, center, distance, angle=0.0):
        super().__init__(intensity_ambient, intensity_diffuse, intensity_specular)
        self._center = center
        self._distance = distance
        self._angle = angle

    def setup(self, id):
        # Set up the rotating light in the scene
        x, y, z, *rest = self._center
        x += self._distance * math.sin(self._angle)
        z += self._distance * math.cos(self._angle)
        self._setup((x, y, z, *rest), id)

    def rotate(self, angle):
        # Rotate the light
        self._angle += angle

# Create instances of PositionedLight and RotatingLight classes for light sources
main_light = PositionedLight(
    position=(0.0, 6.0, 3.0, 0.0),
    intensity_ambient=(0.2, 0.2, 0.2, .0),
    intensity_diffuse=(0.8, 0.8, 0.8, .0),
    intensity_specular=(1.0, 1.0, 1.0, 1.0),
)

secondary_light = RotatingLight(
    center=(0.0, 2.0, 0.0, 1.0),
    distance=6,
    intensity_ambient=(0., 0., 0., 1.0),
    intensity_diffuse=(0.4, .4, .0, .5),
    intensity_specular=(.0, .0, .0, 1.0),
)

# Function to draw a cloud at specified coordinates
def drawCloud(x, y, z, radius):
    glColor3f(1.0, 1.0, 1.0)  # Cloud color (white)
    glPushMatrix()
    glTranslatef(x, y, z)
    glutSolidSphere(radius, 16, 16)  # Adjust the number of slices and stacks for smoother clouds
    glPopMatrix()

# Function to draw multiple clouds
def drawClouds():
    drawCloud(5, 8, 0, 1)
    drawCloud(-8, 10, 3, 1.5)
    drawCloud(-3, 6, -5, 1.2)

# Function to set the background color
def background():
    glClearColor(0.1, 0.1, 0.1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

# Function to set the perspective projection matrix
def perspective():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    _, _, width, height = glGetDoublev(GL_VIEWPORT)
    gluPerspective(45, width / height, 4, 40)

# Function to set the view matrix based on the camera position
def lookat():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    camera.lookat((0, 0, 0))

# Function to set up lighting
def light():
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.2, 0.2, 0.2, 1.0))
    glEnable(GL_LIGHTING)

    main_light.setup(GL_LIGHT0)
    secondary_light.setup(GL_LIGHT1)

# Function to enable depth testing
def depth():
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

# Function to set material properties for the home
def homeMaterial():
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.65, 0.35, 0.25, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.75, 0.45, 0.35, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.8, 0.8, 0.8, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(10.0))

# Function to set material properties for the car
def carMaterial():
    glMaterialfv(GL_FRONT, GL_AMBIENT, GLfloat_4(0.1, 0.1, 0.1, 0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, GLfloat_4(0.8, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, GLfloat_4(0.9, 0.9, 0.9, 0.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, GLfloat(25.0))

# Function to draw a house
def drawHouse():
    homeMaterial()
    glPushMatrix()
    glTranslate(0, 1, -0.5)
    glutSolidCube(2)

    # Front Window
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(0, 0.5, 1.01)
    glScalef(0.8, 0.8, 0.1)
    glutSolidCube(1)
    glPopMatrix()

    # Side Windows
    glPushMatrix()
    glTranslatef(1.01, 0.5, 0)
    glScalef(0.1, 0.8, 0.8)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.01, 0.5, 0)
    glScalef(0.1, 0.8, 0.8)
    glutSolidCube(1)
    glPopMatrix()

    drawRoof(1.5, 1.25, 16, 8)
    drawChimney(0.25)
    glPushMatrix()
    glTranslate(0.8, -0.5, 1.01)
    glScalef(0.4, 1, 0.05)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslate(-0.8, 0, 1.01)
    glScalef(0.4, 0.4, 0.05)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslate(0, 1.2, 2)
    glRotatef(45, 0, 1, 0)
    glutSolidTorus(0.1, 0.2, 8, 8)
    glPopMatrix()
    glPopMatrix()

# Function to draw a roof
def drawRoof(radius, height, slices, stacks):
    glPushMatrix()
    glTranslatef(0, 1, 0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(radius, height, slices, stacks)
    glPopMatrix()

# Function to draw a chimney
def drawChimney(size):
    glPushMatrix()
    glTranslatef(0.5, 1.5, -0.5)
    glScalef(1, 4, 1)
    glutSolidCube(size)
    glPopMatrix()

# Function to draw the moving car
def drawCar():
    # Set material properties and draw the moving car
    carMaterial()
    car.draw()

# Function to display the scene
def display():
    background()
    perspective()
    lookat()
    light()
    depth()
    drawHouse()
    drawCar()
    drawStationaryCar()
    drawClouds()
    glutSwapBuffers()

# Function to update the car position and light rotation in the idle state
def idle_func():
    car.move()
    secondary_light.rotate(0.05)
    glutPostRedisplay()
    time.sleep(0.016)

# Function to handle keydown events
def on_keydown(key, *args):
    if key == GLUT_KEY_RIGHT:
        camera.rotate(0.1)
    elif key == GLUT_KEY_LEFT:
        camera.rotate(-0.1)
    if key == GLUT_KEY_UP:
        camera.move(-0.1)
    elif key == GLUT_KEY_DOWN:
        camera.move(0.1)
    glutPostRedisplay()

# Initialize OpenGL and set up the window
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
# glutInitWindowSize(500, 500) # Set the initial window size to 500x500 pixels
glutCreateWindow(b"Car drifts around house whole day")
glClearColor(0.0, 0.0, 0.0, 0.0)
# glutInitWindowPosition(50, 50) # Set the initial window position to (50, 50) on the screen
glutDisplayFunc(display)
glutFullScreen() # Enable full-screen mode
glutIdleFunc(idle_func)
glutSpecialFunc(on_keydown)
glutMainLoop()
