from State import *
from Event import *

        # If used for manual tests, input desired inches (no need to multiply by 30)
        # self.move_to assumed starting position is 31.16666 and 41.16666 aka (935 / 30 + 6), (1235 / 30 + 6)

class ShowcaseState(State):
    async def enter(self):
        await super().enter()

        # # wait for start LED command here, maybe some sort of signal?
        # await self.move_forward(3, True)
        # #await self.expand_rover()
        # await self.rover_wait(0.5)
        # await self.rotate_left(60)
        # await self.rover_wait(0.1)
        # await self.move_forward(14.5)
        # await self.rover_wait(0.5)
        # await self.rotate_right(70)
        # await self.rover_wait(0.1)
        # await self.move_forward(11)
        # await self.rover_wait(0.1)
        # await self.rover_wait(6) # simulating beacon placement
        # await self.rover_wait(0.1)


        # await self.move_to((self.STARTING_X - 14), (self.STARTING_Y + 10), True)
        # await self.rover_wait(2)
        # await self.move_to((self.STARTING_X + 20), (self.STARTING_Y + 2), True)
        # await self.rover_wait(3)
        # await self.rotate_to(90)

        while True:
            await self.move_to((self.STARTING_X + 0), (self.STARTING_Y + 12), True)
            await self.rover_wait(2)
            await self.move_to((self.STARTING_X + 12), (self.STARTING_Y + 12), True)
            await self.rover_wait(3)
            await self.move_to((self.STARTING_X + 6), (self.STARTING_Y + 6), True)
            await self.rover_wait(3)

            # await self.move_to((self.STARTING_X + 5), (self.STARTING_Y + 6), True)
            # await self.rover_wait(1)
            # await self.move_to((self.STARTING_X + 7), (self.STARTING_Y + 4), True)
            # await self.rover_wait(1)
           # await self.rotate_to(0, True)
           # await self.rover_wait(1)
          #  await self.rotate_to(180, True)
          #  await self.rover_wait(1)

        self.done.emit()


class WaitState(State):
    async def enter(self):
        await super().enter()
        while not self.request_light_detected.emit()[0]:
            await asyncio.sleep(0.1)
        self.done.emit()


class SenseState(State):
    async def enter(self):
        await super().enter()

        await self.move_forward(3, True)
        # await self.expand_rover() # Uncomment this once the robot is finished

        self.done.emit()


class BeaconState(State):
    async def enter(self):
        await super().enter()

        # go to wall
        # run along wall
        # plant beacon

        await self.rover_wait(1)
        await self.move_to(-21.8, 18.8, True)
        await self.rover_wait(1)
        await self.rotate_to(0)
        await self.rover_wait(1)
        await self.rover_wait(0)  # TODO: add simple beacon command to state

        #self.done.emit()

class GCSCState(State):
    async def enter(self):
        await super().enter()

        # while loop contingent on csc load
        # go in front of csc (with front facing away)
        # move_back
        # send load csc event

        await self.rover_wait(1)
        await self.move_to(15, 5.7)
        await self.rover_wait(1)
        await self.rotate_to(270)
        await self.move_back(5)  # TODO: check if this is good
        await self.load_gsc()
        await self.rover_wait(1)

        # self.done.emit()


class NCSCState(State):
    async def enter(self):
        await super().enter()

        await self.rover_wait(1)
        await self.move_to(-6.8, 33.3, True)
        await self.rover_wait(1)
        await self.rotate_to(180)
        await self.move_back(5)  # TODO: check if this is good
        await self.load_nsc()
        await self.rover_wait(1)

        self.done.emit()


class CavePrepState(State):
    async def enter(self):
        await super().enter()

        # go in front of cave
        # rotate to align with cave
        # move forward into cave

        await self.rover_wait(1)
        await self.move_to(35.3, 33.8, True)
        await self.rover_wait(1)
        await self.rotate_to(90)
        await self.move_forward(5)
        await self.load_nsc()
        await self.rover_wait(1)

        self.done.emit()


class CaveVacuumState(State):
    async def enter(self):
        await super().enter()

        # try to exhaustively sweep cave
        # Get ready to leave cave
        # check time after each command, and leave cave if there's not enough. (time to check to be

        ready_position = Event(EventType.TRANSFORM, Transform(Vector3(-300, 0, 0)))
        self.transform_request.emit(ready_position)

        clockwise_turn = Event(EventType.TRANSFORM, Transform(Vector3(0, 0, -90)))
        self.transform_request.emit(clockwise_turn)

        sweep_up = Event(EventType.TRANSFORM, Transform(Vector3(0, 350, 0)))
        self.transform_request.emit(sweep_up)

        back = Event(EventType.TRANSFORM, Transform(Vector3(0, -350, 0)))
        self.transform_request.emit(back)

        move = Event(EventType.TRANSFORM, Transform(Vector3(300, 0, 90)))
        self.transform_request.emit(move)

        self.transform_request.emit(clockwise_turn)
        self.transform_request.emit(sweep_up)
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(-100, 0, 0))))
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(100, 0, 90))))
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(-100, 0, 0))))
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(0, 0, 90))))

        move_down = Event(EventType.TRANSFORM, Transform(Vector3(0, 600, 0)))
        self.transform_request.emit(move_down)
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(100, 0, -90))))
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(-100, 0, 90))))
        self.transform_request.emit(Event(EventType.TRANSFORM, Transform(Vector3(0, -250, 0))))

        move_left = Event(EventType.TRANSFORM, Transform(Vector3(250, 0, 90)))
        self.transform_request.emit(move_left)

        sweep_down = Event(EventType.TRANSFORM, Transform(Vector3(350, 0, -90)))
        self.transform_request.emit(sweep_down)

        self.transform_request.emit(back)

        counter_turn = Event(EventType.TRANSFORM, Transform(Vector3(0, 0, 270), True))
        self.transform_request.emit(counter_turn)

        exit_cave = Event(EventType.TRANSFORM, Transform(Vector3(600, 0, 0)))
        self.transform_request.emit(exit_cave)

        self.done.emit()


class MaterialPickupState(State):
    def __init__(self):
        super().__init__()
        # read april tag
        # find materials
        self.find_path = self.add_signal("find_path")

    async def enter(self):
        # some kind of while loop contingent on time and
        await super().enter()
        self.find_path.emit()
        self.done.emit()
