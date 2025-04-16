import time

from State import *
from Event import *

        # TODO: test start_led

"""
HOW TO USE THIS PAGE:
This is really the only page you need to know how to use (except maybe statemachine.py). If you'd like to alter the
sequence of states that the robot goes through, go to statemachine.py and alter the self.state_list to be in the
order you'd like. 

There is 1 universal command, 4 relative commands, 2 absolute commands and a couple more situational ones.

Also, for any given command, you'll need to add 'await self.' beforehand. Example:
await self.move_forward(3, True)
await self.rover_wait(5)
await self.rotate_to(54, False)
await self.move_to(36, 36)
await self.unleash_beacon() # defaults to True


UNIVERSAL COMMANDS:
rover_wait(seconds) -
Waits a certain time between commands. (NOTE: needs previous command to wait)




RELATIVE COMMANDS (DO NOT USE THESE IDEALLY, THEY DON'T USE OTOS FEEDBACK):
move_forward(distance, wait) - 
Distance is distance forward (negative moves the rover back). 
Wait is defaulted to true, and makes it so that the next command does not queue until this one is complete 
(in case of rover_waits [see below])

move_back(distance, wait) -
Distance is distance backwards (negative numbers theoretically move the rover forward, but is bad practice).
See above for wait parameter.

rotate_right(degrees, wait) -
Degrees rotates the robot that amount of degrees right (negative rotates rover left)
See above for wait parameter.

rotate_left(degrees, wait) -
Degrees rotates the robot that amount of degrees left (negative numbers theoretically rotate left, but is bad practice)
See above for wait parameter


ABSOLUTE COMMANDS:
move_to(pos x, pos y, wait) - 
This moves to an absolute grid point (where the robot is the origin, starting at 0 in. x, 0 in. y)
X (in inches). Left of the origin is negative, right is positive.
Y (in inches). All feasible coordinates are positive.
Wait is defaulted to true, and makes it so that the next command does not queue until this one is complete 
(in case of rover_waits [see below])

rotate_to(rotation, wait) -
This rotates to an absolute degree rotation relative to the starting position. (The robot starts at 0 deg. rotation)
Rotation - just enter a positive degree amount, the program will find the shortest path to the desired rotation.
See above for wait parameter


SITUATIONAL COMMANDS:
NOTE - see above for information about wait parameter
expand_rover(wait) -
Expands cosmic shipping container gripper servos. Might do some other things? The basic idea is that it gets the robot
ready after moving out of the start zone.

load_gsc(wait) - 
Retracts GSC grippers until both the pressure sensor on grippers and limit switch on arm both activate. At the moment,
will repeat until it grabs. By the time you're reading this, it might repeat some other way, you should ask

load_nsc(wait) -
see load_GSC

unleash_beacon(wait) - 
Rotates beacon arm, and then releases beacon.

read_april_tags() - # Returns int
Reads in front of it for an april tag between 0 and 4. Returns that number as an int.

get_material_positions() - # Returns list[Vector2]
Reads in front of it for purple colored things, and returns a list of the positions for those purple things on the 
absolute grid.

get_wall_distance() - # Returns int
Gets the distance to the closest point on the wall. Not used at the moment. It'd be nice to use this, but not enough
time.

"""

class ShowcaseState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 99999999
        self.reset_tracking = self.add_signal("reset_tracking")

    async def enter(self):
        await super().enter()


        light_detected = self.request_light_detected.emit()[0]
        while not light_detected[0]:
            await asyncio.sleep(1)
            light_detected = self.request_light_detected.emit()[0]
        light_detected = 0

        self.reset_tracking.emit()
        await asyncio.sleep(1)

        await self.expand_rover()

        await self.precise_move_to(-13,5)
        await self.precise_move_to(-22.5,18)      # original is -20, 18
        await self.rotate_to(0)
        self.logger.debug("BEACON")
        await self.rotate_to(0)
        await self.rover_wait(0.2)
        await self.unleash_beacon()
        await self.move_to(-20,24)
        await self.move_to_nsc()
        self.logger.debug("NEBULITE")
        await self.load_nsc()
        await self.move_to(1, 18)
        await self.move_to(15, 18)
        #await self.rotate_to(90)
        self.logger.debug("CAVE")
        await self.move_to(19, 18) # poke our head into the cave
        await self.move_event(-1) # exit cave
        await self.rotate_to(270)
        await self.move_to(1, 18)
        await self.move_to(15, 18)
        await self.move_to(1, 18)
        await self.move_to(15, 18)
        # add sweeping
        april_tag = await self.read_april_tags()
        await self.move_to(-15,18)
        match april_tag:
            case 0:
                await self.rotate_to(180)
                await self.move_event(-1) #
            case 1:
                await self.rotate_to(180)
                await self.move_event(-0.5) #
            case 2:
                await self.rotate_to(90)
            case 3:
                await self.rotate_to(270)
                await self.move_event(-0.5) #
            case 4:
                await self.rotate_to(270)
                await self.move_event(-1) #
            case __:
                await self.rotate_to(90)



        light_detected = self.request_light_detected.emit()[0]
        while not light_detected[0]:
            await asyncio.sleep(1)
            light_detected = self.request_light_detected.emit()[0]
        light_detected = 0

        await self.expand_rover()

        #
        #
        # self.done.emit()


class WaitState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 99999999

    async def enter(self):
        await super().enter()
        while not self.request_light_detected.emit()[0]:
            await asyncio.sleep(0.1)
        self.done.emit()


class SenseState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 99999999

    async def enter(self):
        await super().enter()

        await self.move_forward(3, True)
        # await self.expand_rover() # Uncomment this once the robot is finished

        self.done.emit()


class BeaconState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 99999999

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
        #await self.unleash_beacon()  # Uncomment this when beacon is working

        #self.done.emit()

class GCSCState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 99999999

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
        await self.move_back(5)

        completed = await self.load_gsc()
        while not completed:
            await self.rover_wait(1)
            await self.move_to(-6.8, 33.3, True)
            await self.rover_wait(1)
            await self.rotate_to(180)
            await self.move_back(5)
            completed = await self.load_gsc()
        await self.rover_wait(1)

        # self.done.emit()


class NCSCState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 280

    async def enter(self):
        await super().enter()

        await self.rover_wait(1)
        await self.move_to(-6.8, 33.3, True)
        await self.rover_wait(1)
        await self.rotate_to(180)
        await self.move_back(5)

        completed = await self.load_nsc()
        while not completed:
            await self.rover_wait(1)
            await self.move_to(-6.8, 33.3, True)
            await self.rover_wait(1)
            await self.rotate_to(180)
            await self.move_back(5)
            completed = await self.load_nsc()

        await self.rover_wait(1)

        self.done.emit()


class CavePrepState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 280

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
    def __init__(self):
        super().__init__()  # TODO: Might need a custom emergency exit state.
        self.ending_time = 275

    # 24.5, 16.5
    # 32.35, 1
    # 46.64, 1
    # 46.64, 37.09
    # 32.35, 37.09
    # 32.35, 16.5

    async def enter(self):
        await super().enter()
        # check time after each command, and leave cave if there's not enough. (time to check to be
        await self.move_to(24.5, 16.5)  # Entrance of cave

       # COORD 1
        await self.move_to(32.35, 16.5) # Go forward a bit
        await self.move_to(32.35, 1) # Sweep
        await self.move_back(15.5) # Back up
        await self.move_to(46.64, 16.5) # Get ready for next part

        # COORD 2
        await self.move_to(46.64, 1)
        await self.move_back(15.5)
        await self.rotate_right(180)

        # COORD 3
        await self.move_to(46.64, 37.09)
        await self.move_back(15.5)
        await self.move_to(32.35, 16.5)

        # COORD 4
        await self.move_to(32.35, 37.09)
        await self.move_back(15.5)

        # LEAVE CAVE
        await self.move_to(32.35, 16.5) # Get ready to leave cave
        await self.move_to(24.6, 16.5)
        self.done.emit()



class MaterialPickupState(State):
    def __init__(self):
        super().__init__()
        self.ending_time = 280
        self.find_path = self.add_signal("find_path")

    async def enter(self):
        # some kind of while loop contingent on time and
        await super().enter()

        if self.exit_if_over_time(self.ending_time):
            return

        loading_zone_number = await self.read_april_tags()
        self.april_tag_found(loading_zone_number)  # Checks if we're over time

        material_positions = self.get_material_positions()
        if len(material_positions) == 0:
            pass


        self.find_path.emit()
        self.done.emit()

    async def find_april_tag(self):
        pass
