from dataclasses import dataclass
from Event import *
import asyncio
import math
import logging


@dataclass
class Vector2:
    """Represents a 2D vector."""
    x: float
    y: float

    def length(self) -> float:
        """Returns the length of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, other: 'Vector2') -> float:
        """Returns the distance to another vector."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: int) -> 'Vector2':
        return Vector2(self.x * multiplier, self.y * multiplier)

    def __truediv__(self, divisor: int):
        return Vector2(self.x / divisor, self.y / divisor)

    @staticmethod
    def ZERO():
        return Vector2(0, 0)


class Vector3:
    def __init__(self, x: float = 0, y: float = 0, rot: float = 0):
        self.x = x
        self.y = y
        self.rot = rot

    def get_position(self) -> Vector2:
        return Vector2(self.x, self.y)

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.rot + other.rot)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.rot - other.rot)

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}, rot: {self.rot}"

    @staticmethod
    def ZERO():
        return Vector3(0, 0, 0)


class Transform(SignalEmitter):
    class PositionType(Enum):
        ABSOLUTE = 1
        RELATIVE = 2

    def __init__(self, transform: Vector3 = Vector3.ZERO(), absolute: bool = False):
        SignalEmitter.__init__(self)
        self.position = Vector2(transform.x, transform.y)
        self.rotation = transform.rot
        self.type = self.PositionType.ABSOLUTE if absolute else self.PositionType.RELATIVE
        self.position_reached = asyncio.Event()

    def __str__(self):
        return str("X:" + str(self.position.x) + " Y: " + str(self.position.y) + " Rot:" + str(self.rotation) +
                   " Absolute: " + str(self.type))

    def is_absolute(self) -> bool:
        return self.type == self.PositionType.ABSOLUTE

    def get_position(self) -> Vector2:
        return self.position

    def get_vector3(self) -> Vector3:
        return Vector3(self.position.x, self.position.y, self.rotation)

    def get_rotation_to_target(self, target_position: Vector2) -> float: # Maybe this one (probably)
        """
        Calculates the rotation needed to face the target position.
        """
        if target_position == self.position:
            return 0
        logger = logging.getLogger("Nano")
        logger.debug("Get_rotation_to_target - ")
        logger.debug("Current Pos: " + str(self.position))
        logger.debug("Target Pos: " + str(target_position))

        direction = target_position - self.position
        angle_radians = math.atan2(direction.x, direction.y)        # DM flipped x and y (x/y). This causes positive angle to be from y clockwise

        logger.debug("Direction: " + str(direction))
        logger.debug("Angle: " + str(math.degrees(angle_radians)))
        angle_degrees = math.degrees(angle_radians)                 # DM removed 180 - angle
        while angle_degrees < 0:
            angle_degrees += 360
        while angle_degrees > 360:
            angle_degrees -= 360
        logger.debug("Angle: " + str(angle_degrees))
        return angle_degrees


    def get_shortest_rotation_to(self, target_rotation: float) -> float:
        """
        Calculates the shortest rotation to the target angle.
        """
        logger = logging.getLogger("Nano")
        logger.debug("Get_shortest_rotation_to - ")
        logger.debug(f"Current Rotation: {str(self.rotation)}")
        logger.debug("Target rotation: " + str(target_rotation))

        target_rotation = target_rotation % 360
        direct_rotation = target_rotation - self.rotation

        direct_rotation = direct_rotation
        while direct_rotation < -180:
            direct_rotation += 360
        while direct_rotation > 180:
            direct_rotation -= 360
        logging.debug(f"Shortest rotation to target rotation: {direct_rotation}")
        return direct_rotation


class State(SignalEmitter):
    STARTING_X = 0
    STARTING_Y = 0

    def __init__(self):
        SignalEmitter.__init__(self)
        self.entered_state = self.add_signal("entered_state")
        self.exited_state = self.add_signal("exited_state")
        self.done = self.add_signal("done")
        self.transform_request = self.add_signal("transform_request")
        self.request_light_detected = self.add_signal("request_light_detected")

    async def enter(self):
        self.entered_state.emit(self)
        logger = logging.getLogger("Nano")
        logger.info("Entered State: " + str(self.__class__.__name__))

    async def exit(self):
        self.exited_state.emit(self)
        logger = logging.getLogger("Nano")
        logger.info("Exited State: " + str(self.__class__.__name__))

    async def update(self, delta: float):
        pass

    async def move_forward(self, distance: float, wait=False) -> None:
        """
        Moves the robot the specified distance forward in inches
        """
        if distance > 0:
            logging.debug(f"Translating {distance} inches forward.")
        elif distance < 0:
            logging.debug(f"Translating {abs(distance)} inches back.")
        else:
            logging.debug("Received 0 inches for movement")
        move_forward = Event(EventType.MOVE, distance)
        self.transform_request.emit(move_forward)
        if wait:
            await move_forward.event_finished.wait()  # This is related to  AsyncIO

    async def move_back(self, distance: float, wait=False) -> None:
        """
        Moves the robot the specified distance backwards in inches
        """
        await self.move_forward(-distance, wait)

    async def move_to(self, x: float, y: float, wait=False) -> None:
        """
        Moves to an absolute position on the grid
        :param x: Desired x position on grid (in inches)
        :param y: Desired y position on grid (in inches)
        :param wait: Should the robot wait to issue the next command after this function?
        """
        position = Vector2(x, y)
        move_event = Event(EventType.TRANSFORM, Transform(Vector3(position.x, position.y, 0), True))
        self.transform_request.emit(move_event)
        if wait:
            await move_event.event_finished.wait()  # This is related to  AsyncIO

    async def rotate_right(self, angle: float, wait=False) -> None:
        """
        Moves the robot the specified angle right in degrees
        """
        if angle > 0:
            logging.debug(f"Rotating {angle} degrees to the right")
        elif angle < 0:
            logging.debug(f"Rotating {abs(angle)} degrees to the left")
        else:
            logging.debug("Received 0 degrees for rotation")
        rotate_right = Event(EventType.ROTATE, angle)
        self.transform_request.emit(rotate_right)
        if wait:
            await rotate_right.event_finished.wait()  # This is related to  AsyncIO

    async def rotate_left(self, angle: float, wait=False) -> None:
        """
        Moves the robot the specified angle left in degrees
        """
        await self.rotate_right(-angle, wait)

    async def rotate_to(self, angle: int, wait=False) -> None:
        """
        Rotates the robot to a given 'absolute' angle. (0 is starting rotation, 90 is towards cave)
        :param angle: Angle in degrees
        :param wait: Wait for event to finish before queueing next event
        :return: None
        """
        logging.debug(f"Rotating to {angle}")
        absolute_rotate = Event(EventType.ABSOLUTE_ROTATE, angle)
        self.transform_request.emit(absolute_rotate)
        if wait:
            await absolute_rotate.event_finished.wait()

    async def rover_wait(self, seconds: float) -> None:
        """
        Waits a period of time before moving again. Needs previous command to have wait=true
        :param seconds: Wait time in seconds
        """
        logging.debug(f"Waiting {seconds} seconds")
        await asyncio.sleep(seconds)

    async def expand_rover(self, wait = True) -> None:
        """
        WIP.
        :param wait: Do we wait for the rover to expand before queueing next command
        :return: None
        """
        expand_event = Event(EventType.EXPAND, 0)
        self.transform_request.emit(expand_event)
        if wait:
            await expand_event.event_finished.wait()

    async def load_gsc(self, wait = True) -> None:
        completed = False
        while not completed:
            load_event = Event(EventType.LOAD, 0)
            self.transform_request.emit(load_event)
            if wait:
                await load_event.event_finished.wait()
            if load_event.event_success:
                completed = True

    async def load_nsc(self, wait = True) -> None:  # TODO: change this so that it relocates to starting pos
        completed = False
        while not completed:
            load_event = Event(EventType.LOAD, 1)
            self.transform_request.emit(load_event)
            if wait:
                await load_event.event_finished.wait()
            if load_event.event_success:
                completed = True

    async def find_path(self, iteration,  wait = True) -> None:
        pathfind_event = Event(EventType.FIND_PATH, iteration)
        self.transform_request.emit(pathfind_event)
        if wait:
            await pathfind_event.event_finished.wait()

            """
            expand_robot
            GSC_load
            NSC_load
            event_failed,GSC_load,
            """

