from dataclasses import dataclass
from types import coroutine

from Event import *
import asyncio
import math
import logging
import time
from control import *


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

    def __eq__(self, other):
        print("test")
        return (self.x == other.x) and (self.y == other.y)

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
        logger.debug(f"Shortest rotation to target rotation: {direct_rotation}")
        return direct_rotation


class State(SignalEmitter):
    STARTING_X = 0
    STARTING_Y = 0

    def __init__(self):
        SignalEmitter.__init__(self)
        self.starting_time = 0
        self.ending_time = 99999
        self.entered_state = self.add_signal("entered_state")
        self.exited_state = self.add_signal("exited_state")
        self.done = self.add_signal("done")
        self.transform_request = self.add_signal("transform_request")
        self.request_light_detected = self.add_signal("request_light_detected")
        self.request_loading_zone = self.add_signal("request_loading_zone")
        self.april_tag_found = self.add_signal("april_tag_found")
        self.request_emergency_exit = self.add_signal("request_emergency_exit")
        self.request_path = self.add_signal("request_path")
        self.mark_point = self.add_signal("mark_point")
        self.request_current_transform = self.add_signal("request_current_transform")
        self.logger = logging.getLogger("Nano")


        self.COMMAND_LIST = {"expand_rover": self.expand_rover, "load_gsc": self.load_gsc, "load_nsc": self.load_nsc,
                        "unleash_beacon": self.unleash_beacon, "read_april_tags": self.read_april_tags,
                        "get_material_positions": self.get_material_positions,
                        "get_wall_distance": self.get_wall_distance}


    async def enter(self):
        self.entered_state.emit(self)
        self.logger.info("Entered State: " + str(self.__class__.__name__))
        if await self.exit_if_over_time(self.ending_time):
            return

    async def exit(self):
        self.exited_state.emit(self)
        self.logger.info("Exited State: " + str(self.__class__.__name__))

    async def check_timer(self, time_limit: int) -> bool:
       if (time.time() - self.starting_time) >= time_limit:
           return True
       else:
           return False

    async def emergency_exit(self):
        self.request_emergency_exit.emit()
        self.done.emit()

    async def exit_if_over_time(self, time_limit: int) -> bool:
        if await self.check_timer(time_limit):
            await self.emergency_exit()
            return True
        else:
            return False

    async def move_forward(self, distance: float, wait=True) -> None: # TODO: FIX FOR NEW SYSTEM
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

    async def move_back(self, distance: float, wait=True) -> None: # TODO: FIX FOR NEW SYSTEM
        """
        Moves the robot the specified distance backwards in inches
        """
        await self.move_forward(-distance, wait)

    async def move_to(self, x: float, y: float, wait=True) -> None:
        """
        Moves to an absolute position on the grid
        :param x: Desired x position on grid (in inches)
        :param y: Desired y position on grid (in inches)
        :param wait: Should the robot wait to issue the next command after this function?
        """
        target_position = Transform(Vector3(x,y,0))
        current_position: Transform = self.request_current_transform.emit()[0][0]
        target_angle = current_position.get_rotation_to_target(target_position.get_position())

        if not self._rot_is_close_enough(target_angle, current_position.rotation):
            await self.rotate_to(target_angle)

        move_event = Event(EventType.MOVE, target_position)
        self.transform_request.emit(move_event)
        if wait:
            await move_event.event_finished.wait()  # This is related to AsyncIO

    async def precise_move_to(self, x: float, y: float, wait=True) -> None:
        """
        Moves to an absolute position on the grid
        :param x: Desired x position on grid (in inches)
        :param y: Desired y position on grid (in inches)
        :param wait: Should the robot wait to issue the next command after this function?
        """
        target_position = Transform(Vector3(x,y,0))
        current_position: Transform = self.request_current_transform.emit()[0][0]
        target_angle = current_position.get_rotation_to_target(target_position.get_position())

        if not self._rot_is_close_enough(target_angle, current_position.rotation):
            await self.rotate_to(target_angle)

        move_event = Event(EventType.PRECISE_MOVE, target_position)
        self.transform_request.emit(move_event)
        if wait:
            await move_event.event_finished.wait()  # This is related to AsyncIO

    async def move_event(self, duration, wait = True) -> None:
        # idk smth about moving forward and backward based on the positive or negative duration in seconds

        move_event = Event(EventType.RELATIVE_MOVE, duration)
        self.transform_request.emit(move_event)
        if wait:
            await move_event.event_finished.wait()  # This is related to AsyncIO


    async def move_to_gsc(self) -> None:
        await self.move_to(0,0) # TODO: change this
        await self.rotate_to(270)

    async def move_to_nsc(self) -> None:
        await self.move_to(-1.0,24)
        await self.rotate_to(180)

    async def rotate_right(self, angle: float, wait=True) -> None: # TODO: FIX FOR NEW SYSTEM
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

    async def rotate_left(self, angle: float, wait=True) -> None: # TODO: FIX FOR NEW SYSTEM
        """
        Moves the robot the specified angle left in degrees
        """
        await self.rotate_right(-angle, wait)

    async def rotate_to(self, angle: float, wait=True) -> None:
        """
        Rotates the robot to a given 'absolute' angle. (0 is starting rotation, 90 is towards cave)
        :param angle: Angle in degrees
        :param wait: Wait for event to finish before queueing next event
        :return: None
        """
        self.logger.debug(f"Rotating to {angle}")
        absolute_rotate = Event(EventType.ROTATE, angle)
        self.transform_request.emit(absolute_rotate)
        if wait:
            await absolute_rotate.event_finished.wait()

    async def rover_wait(self, seconds: float) -> None:
        """
        Waits a period of time before moving again. Needs previous command to have wait=true
        :param seconds: Wait time in seconds
        """
        self.logger.debug(f"Waiting {seconds} seconds")
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

    async def retract_rover(self):
        retract_event = Event(EventType.RETRACT, 0)
        self.transform_request.emit(retract_event)
        await retract_event.event_finished.wait()

    async def load_gsc(self, wait = True) -> bool:
        load_event = Event(EventType.LOAD, 0)
        self.transform_request.emit(load_event)
        if wait:
            await load_event.event_finished.wait()

    async def load_nsc(self, wait = True) -> bool:
        load_event = Event(EventType.LOAD, 1)
        self.transform_request.emit(load_event)
        if wait:
            await load_event.event_finished.wait()

    async def unleash_beacon(self, wait = True) -> None:
        beacon_event = Event(EventType.BEACON, 0)
        self.transform_request.emit(beacon_event)
        if wait:
            await beacon_event.event_finished.wait()

    async def read_april_tags(self) -> int:
        april_tag = control(0, 0, 1)

        if april_tag < 0:
            await self.move_forward(3, True)
            april_tag = control(0, 0, 1)
            # The below statement makes sure that we're not going to overrun on time, even if we bug out.
            while april_tag < 0 and not await self.exit_if_over_time(self.ending_time-15):
                await self.rotate_left(10, True)
                april_tag = control(0, 0, 1) if control(0, 0, 1) > 0 else april_tag
                await self.rotate_right(10, True)
                april_tag = control(0, 0, 1) if control(0, 0, 1) > 0 else april_tag

        return control(0, 0, 1)


    @staticmethod
    async def get_material_positions() -> list:
        return control(0, 1, 0)

    @staticmethod
    async def get_wall_distance() -> int:
        return control(1, 0, 0)

    @staticmethod
    def _rot_is_close_enough(current_rot, target_rot, close_enough_rotation=5):
        target_rotation_plus = target_rot + 360
        target_rotation_minus = target_rot - 360
        if abs(current_rot - target_rot) <= close_enough_rotation:
            return True
        elif abs(current_rot - target_rotation_plus) <= close_enough_rotation:
            return True
        elif abs(current_rot - target_rotation_minus) <= close_enough_rotation:
            return True
        else:
            return False
