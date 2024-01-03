import pygame
import pymunk
import pymunk.pygame_util
from math import sin, cos, asin, radians, degrees, sqrt
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    floor_height,
    gravity,
    bird_position,
    bird_radius,
    aiming_range
)
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


def convert_coords(coords):
    """
    Converts coordinates in such a way that it moves horizontal axis
    from the bottom of display to the top or vice versa.
    Vertical axis stays the same and it is located on the left of the diplay.
    The function is needed because pygame has its horizontal axis at the top of display,
    while pymunk on the bottom.
    """
    x, y = coords
    return (x, SCREEN_HEIGHT - y)


def check_coords(coords):
    """
    If given coordinates are invalid raises CoordinatesError.
    Coordinates are invlaid when one of them is negative
    or is bigger than screen size.
    """
    x, y = coords
    if x < 0 or y < 0 or x > SCREEN_WIDTH or y > SCREEN_HEIGHT:
        raise CoordinatesError(coords)


def check_radius(radius):
    """
    Raises ValueError if radius is not positive.
    """
    if radius <= 0:
        raise ValueError('Radius has to be positive')


def space_draw(space: pymunk.Space, options):
    """
    Draws all elements in pymunk's space on pygame's display.
    """
    space.debug_draw(options)


def calc_distance_and_angle(point1: int, point2: int):
    """
    Calculates distance between two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    angle = degrees(asin(abs(y1 - y2) / distance))
    return min(distance, aiming_range), angle


def is_on_circle(circle_position, radius, point):
    """
    Returns True if given point is inside a circle with the center in circle_position
    and given radius.
    Otherwise it return False.
    """
    a, b = circle_position
    x, y = point
    if round((x - a)**2 + (y - b)**2) <= round(radius ** 2):
        return True
    return False


class CoordinatesError(Exception):
    """
    Class CoordinatesError.
    Class inherits attributes from Exception class.
    Contains attributes:
    :param coordinates: invalid coordinates
    :type coordinates: tuple
    """
    def __init__(self, coords):
        """
        Creates instance of error.
        """
        super().__init__('Invalid coordinates')
        self.coordinates = coords


class Bird:
    """
    Class Bird. Contains attributes:
    :param body: pymunk body of the bird
    :type body: pymunk.body.Body

    :param shape: pymunk shape of the bird
    :type shape: pymunk.shapes.Circle

    :param radius: radius of the bird
    :type radius: int

    :param velocity: initial velocity of the bird set by set_speed method, defualt: 0
    :type velocity: int

    :param angle: initial angle of the bird trajectory set by set_speed method, defualt: 0
    :type angle: int

    :param x_velocity: initial x_velocity of the bird set by set_speed method, defualt: 0
    :type x_velocity: int

    :param x_velocity: initial y_velocity of the bird set by set_speed method, defualt: 0
    :type x_velocity: int
    """
    def __init__(self, space: pymunk.Space, position: tuple, radius: int, density=1, elasticity=1, friction=0):
        """
        Creates instance of Bird.

        Raises ValueError if radius, density or elasticiy is negative.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.
        """
        check_coords(position)
        check_radius(radius)
        if density < 0:
            raise ValueError('Density cannot be negative')
        if elasticity < 0:
            raise ValueError('Elasticity cannot be negative')
        self.body = pymunk.Body()
        self.body.position = position
        self._shape = pymunk.Circle(self.body, radius)
        self._shape.density = density
        self._shape.elasticity = elasticity
        self._shape.friction = friction
        self._shape.collision_type = 1
        self._radius = radius
        self.velocity = 0
        self.angle = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.body.velocity = (self.x_velocity, self.y_velocity)
        space.add(self.body, self.shape)

    @property
    def shape(self):
        """
        Returns shape of the bird.
        """
        return self._shape

    @property
    def radius(self):
        """
        Returns radius of the bird.
        """
        return self._radius

    def set_radius(self, new_radius):
        """
        Changes radius of the bird to new_radius.

        Raises ValueError if new_radius is not positive.
        """
        check_radius(new_radius)
        self._radius = new_radius

    def set_speed(self, pressed_keys, mouse_pos, screen):
        """
        Sets speed of the bird depending on angle and velocity given by user.
        """
        if mouse_pos is None:
            if pressed_keys[K_UP] or pressed_keys[K_w]:
                if self.angle < 360:
                    self.angle += 1
                else:
                    self.angle = 0
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                if self.angle > 0:
                    self.angle -= 1
                else:
                    self.angle = 359
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.velocity += 10
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                if self.velocity > 10:
                    self.velocity -= 10
                else:
                    self.velocity = 0
        else:
            x, y = bird_position
            distance, angle = calc_distance_and_angle(bird_position, mouse_pos)
            if mouse_pos[0] > x and mouse_pos[1] < y:
                self.angle = 180 - angle
            elif mouse_pos[0] > x and mouse_pos[1] > y:
                self.angle = 180 + angle
            elif mouse_pos[0] < x and mouse_pos[1] > y:
                self.angle = 360 - angle
            else:
                self.angle = angle
            line_point = (x + aiming_range * cos(radians(self.angle + 180)),
                          y + aiming_range * sin(radians(self.angle + 180)))
            if is_on_circle(bird_position, aiming_range, mouse_pos):
                pygame.draw.line(screen, (0, 0, 0), convert_coords(mouse_pos), convert_coords(bird_position), 3)
            else:
                pygame.draw.line(screen, (0, 0, 0), convert_coords(line_point), convert_coords(bird_position), 3)
            self.velocity = distance * SCREEN_WIDTH / 400
        self.x_velocity = int(self.velocity * cos(radians(self.angle)))
        self.y_velocity = int(self.velocity * sin(radians(self.angle)))

    # def set_speed(self, pressed_keys):
    #     """
    #     Sets speed of the bird depending on what key has been pressed.
    #     """
    #     if pressed_keys[K_UP] or pressed_keys[K_w]:
    #         self.y_velocity += 10
    #     if pressed_keys[K_DOWN] or pressed_keys[K_s]:
    #         if self.y_velocity > 10:
    #             self.y_velocity -= 10
    #         else:
    #             self.y_velocity = 0
    #     if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
    #         self.x_velocity += 10
    #     if pressed_keys[K_LEFT] or pressed_keys[K_a]:
    #         if self.x_velocity > 10:
    #             self.x_velocity -= 10
    #         else:
    #             self.x_velocity = 0


class Trajectory:
    """
    Class Trajcetory. Contains attributes:
    :param bird: currently used bird
    :type bird: Bird

    :param x_vel: currently set horizontal speed of the bird, defualt: 0
    :type x_vel: int

    :param y_vel: currently set vertical speed of the bird, defualt: 0
    :type y_vel: int

    :param start_point: starting position of the bird
    :type start_point: tuple

    :param vertex: vertex of the trajectory
    :type vertex: tuple

    :param a_of_pattern: first coefficient of quadratic function of trajcetory
    :type x_velocity: float
    """
    def __init__(self, bird: Bird):
        """
        Creates instance of Trajectory.
        """
        self.bird = bird
        self.x_vel = 0
        self.y_vel = 0
        self.start_point = list(bird.body.position)
        self.vertex = list(bird.body.position)
        self.a_of_pattern = 0

    def calc(self):
        """
        Calculates vertex coefficients and "a" coefficient of quadratic function of trajectory
        based of vertical and horizontal speed of the bird.
        """
        self.x_vel = self.bird.x_velocity
        self.y_vel = self.bird.y_velocity
        if self.x_vel and self.y_vel > 0:
            self.vertex[0] = ((self.x_vel * self.y_vel) / -gravity[1]) + self.start_point[0]
            self.vertex[1] = ((self.y_vel ** 2) / (2 * -gravity[1])) + self.start_point[1]
            self.a_of_pattern = (self.start_point[1] - self.vertex[1]) / ((self.start_point[0] - self.vertex[0]) ** 2)

    def draw(self, screen):
        """
        Draws circles on trajectory of the bird based of user input.
        """
        if self.y_vel >= 0:
            interval = int(abs(self.x_vel) / 15) + 1
            if self.x_vel > 0:
                for x in range(bird_position[0], 800, interval):
                    y = self.a_of_pattern * (x - self.vertex[0]) ** 2 + self.vertex[1]
                    if y >= 100 and self.y_vel:
                        pygame.draw.circle(screen, (0, 0, 0), convert_coords((x, y)), 3)
            elif self.x_vel < 0:
                for x in range(-100, bird_position[0], interval):
                    y = self.a_of_pattern * (x - self.vertex[0]) ** 2 + self.vertex[1]
                    if y >= 100 and self.y_vel:
                        pygame.draw.circle(screen, (0, 0, 0), convert_coords((x, y)), 3)
            elif self.y_vel > 0:
                distance = self.y_vel ** 2 / (2 * -gravity[1])
                pygame.draw.circle(screen, (0, 0, 0),
                                   (bird_position[0], SCREEN_HEIGHT - (distance + bird_radius + floor_height)), 3)
                for height in range(0, int(distance), 30):
                    pygame.draw.circle(screen, (0, 0, 0),
                                       (bird_position[0],
                                        SCREEN_HEIGHT - (floor_height + bird_radius + height)), 3)


class Pig:
    def __init__(self, space: pymunk.Space, position: tuple, radius: int):
        """
        Creates instance of pig.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.

        Raises ValueError if raidus is not positive.
        """
        check_coords(position)
        check_radius(radius)
        self.body = pymunk.Body()
        self.body.position = position
        self._radius = radius
        self._shape = pymunk.Circle(self.body, self._radius)
        self._shape.density = 0.8
        self._shape.elasticity = 0.7
        self._shape.friction = 0.8
        self._shape.color = pygame.Color("green")
        self._shape.collision_type = 3
        space.add(self.body, self._shape)

    @property
    def shape(self):
        """
        Returns shape of the pig
        """
        return self._shape

    @property
    def radius(self):
        """
        Returns radius of the pig
        """
        return self._radius

    def set_position(self, new_position):
        """
        Sets position of the pig to new_position.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.
        """
        check_coords(new_position)
        self.body.position = new_position
        self._shape = pymunk.Circle(self.body, self._radius)

    def set_radius(self, new_radius):
        """
        Sets radius of the pig to new_radius.

        Raises ValueError if raidus is not positive.
        """
        check_radius(new_radius)
        self._radius = new_radius
        self._shape = pymunk.Circle(self.body, self._radius)


class Bar:
    """
    Class Bar. Contains attributes:
    :param body: pymunk body of the bar
    :type body: pymunk.body.Body

    :param shape: pymunk shape of the bar
    :type shape: pymunk.shapes.Poly

    :param size: size of the bar
    :type size: tuple
    """
    def __init__(self, space: pymunk.Space, position: tuple, size: tuple, body_type='dynamic', color=(0, 0, 0)):
        """
        Creates instance of bar.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.

        Raises ValueError if size is not positive.

        Raises ValueError if color is invalid.
        """
        check_coords(position)
        if size[0] <= 0 or size[1] <= 0:
            raise ValueError('Size of the bar has to be positive')
        self.size = size
        if body_type == 'dynamic':
            self.body = pymunk.Body()
            self._shape = pymunk.Poly.create_box(self.body, self.size, 2)
            self._shape.color = pygame.Color(color)
        elif body_type == 'static':
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self._shape = pymunk.Poly.create_box(self.body, self.size)
        else:
            raise ValueError('Invalid body_type, has to be static or dynamic')
        self.body.position = position
        self._shape.density = 0.7
        self._shape.elasticity = 0.4
        self._shape.friction = 0.6
        self._shape.collision_type = 4
        space.add(self.body, self.shape)

    @property
    def shape(self):
        """
        Returns pymunk's shape of the bar.
        """
        return self._shape

    def set_position(self, new_position):
        """
        Changes position of the bar to new_position.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.
        """
        check_coords(new_position)
        self.body.position = new_position

    def set_size(self, new_size):
        """
        Changes size of the bar to new_size.

        Raises ValueError if size is not positive.
        """
        if new_size[0] <= 0 or new_size[1] <= 0:
            raise ValueError('Size of the bar has to be positive')
        self.size = new_size
        self._shape = pymunk.Poly.create_box(self.body, self.size, 1)

    def set_color(self, new_color):
        """
        Changes color of the bar to new_color.

        Raises ValueError if color is invalid.
        """
        self._shape.color = pygame.Color(new_color)


class Floor:
    """
    Class Floor. Contains attributes:
    :param body: pymunk body of the floor
    :type body: pymunk.body.Body

    :param shape: pymunk shape of the floor
    :type shape: pymunk.shapes.Segment
    """
    def __init__(self, space: pymunk.Space):
        """
        Creates instance of Floor.
        """
        self._body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self._shape = pymunk.Segment(
            body=self._body,
            a=(-500, 0),
            b=(SCREEN_WIDTH + 500, 0),
            radius=floor_height)
        self._shape.elasticity = 0.6
        self._shape.friction = 0.8
        self._shape.collision_type = 2
        space.add(self.body, self.shape)

    @property
    def body(self):
        """
        Returns body of the floor
        """
        return self._body

    @property
    def shape(self):
        """
        Returns shape of the floor
        """
        return self._shape


class Text:
    """
    Class Text. Contains attributes:
    :param str: content of the text
    :type str: str

    :param position: position of the text
    :type position: tuple

    :param size: font size of the text, defualt: 10
    :type size: int

    :param color: color of the text's symbols, , defualt: (0, 0, 0)
    :type color: tuple

    :param background: background color of the text, defualt: (255, 255, 255)
    :type background: tuple

    :param font_type: system's font of the text, defualt: 'timesnewroman'
    :type font_type: str

    :param font: pygame font object, contains font_type and size
    :type font: pygame.font.SysFont
    """
    def __init__(
            self,
            str: str,
            position: tuple,
            size=10,
            color=(0, 0, 0),
            background=(255, 255, 255),
            font='timesnewroman'
    ):
        """
        Creates instance of Text.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.

        Raises ValueError if size is not positive.

        Raises ValueError if color or background is invalid.
        """
        check_coords(position)
        if size <= 0:
            raise ValueError('Size has to be positive')
        self._str = str
        self._position = position
        self._size = size
        self._color = color
        self._background = background
        self._font_type = font
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    @property
    def str(self):
        """
        Returns str of the text.
        """
        return self._str

    @property
    def position(self):
        """
        Returns position of the text.
        """
        return self._position

    @property
    def size(self):
        """
        Returns size of the text.
        """
        return self._size

    @property
    def color(self):
        """
        Returns color of the text.
        """
        return self._color

    @property
    def background(self):
        """
        Returns background of the text.
        """
        return self._background

    @property
    def font_type(self):
        """
        Returns font_type of the text.
        """
        return self._font_type

    def set_str(self, new_str):
        """
        Changes str of the text to new_str.
        """
        self._str = new_str
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_position(self, new_position):
        """
        Changes position of the text to new_position.

        Raises CoordinatesError if coordinates are negative or bigger than screen size.
        """
        check_coords(new_position)
        self._position = new_position

    def set_size(self, new_size):
        """
        Changes size of the text to new_size.

        Raises ValueError if size is not positive.
        """
        if new_size <= 0:
            raise ValueError('Size has to be positive')
        self._size = new_size
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_color(self, new_color):
        """
        Changes color of the text to new_color.

        Raises ValueError if color is invalid.
        """
        self._color = new_color
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_background(self, new_background):
        """
        Changes background of the text to new_background.

        Raises ValueError if background is invalid.
        """
        self._background = new_background
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def set_font_type(self, new_font_type):
        """
        Changes font_type of the text to new_font_type.
        """
        self._font_type = new_font_type
        self._font = pygame.font.SysFont(self._font_type, self._size)
        self._surf = self._font.render(self._str, True, self._color, self._background)

    def draw(self, screen):
        """
        Draws text on pygame display.
        """
        screen.blit(self._surf, self._position)
