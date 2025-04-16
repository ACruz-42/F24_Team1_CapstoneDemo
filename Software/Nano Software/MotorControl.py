import logging

from State import *
from Signal import *

ANGLE_K = .005
TOL_A = 4

class OutputPacket(SignalEmitter):
    left_wheel_speed:float
    right_wheel_speed:float
    auger_flag: int
    sweeper_flag: int
    beacon_arm_flag: int
    beacon_gripper_flag: int
    gsc_gripper_flag: int
    nsc_gripper_flag: int
    gsc_leaner_flag: int
    nsc_leaner_flag: int

    def __init__(self):
        super().__init__()
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0
        self.auger_flag = 0
        self.sweeper_flag = 0
        self.beacon_arm_flag = 0
        self.beacon_gripper_flag = 0
        self.gsc_gripper_flag = 0
        self.nsc_gripper_flag = 0
        self.gsc_leaner_flag = 0
        self.nsc_leaner_flag = 0

        self.game_started = False
        self.game_ended = True

    def __str__(self):
        return (f"{self.left_wheel_speed},{self.right_wheel_speed},{self.auger_flag},{self.sweeper_flag},"
                +f"{self.beacon_arm_flag},{self.beacon_gripper_flag},0,{self.nsc_gripper_flag},"
                 +f"0,{self.nsc_leaner_flag}"+"\n")

    async def set_motor_speed_translation(self, current_position: Transform, target_position: Transform, direction,
                                          testing = True) -> None:
        angle = current_position.get_rotation_to_target(target_position.get_position())
        move_amount = current_position.position.distance_to(target_position.position)
        speed = 50
        speed = speed * direction
        ramp = move_amount * 0.05

        if testing:
            self.left_wheel_speed = 100
            self.right_wheel_speed = 100

        if angle > 180:
            angle = angle - 360 # this might should be 359, but this will give a negative angle to indicate left drift

        angle_k2 = angle * ANGLE_K # this will give a decreasing factor
        angle_k1 = (angle * ANGLE_K) + 1 # this will give an increasing factor

        # DM - I think this should be (1 + ANGLE_K) * angle and (1-ANGLE_K) * angle


        # this looks like it corrects while translating
        if TOL_A >= angle > -TOL_A:
            self.left_wheel_speed = speed
            self.right_wheel_speed = speed
        elif angle > TOL_A:
            self.left_wheel_speed = speed * angle_k2
            self.right_wheel_speed = speed * angle_k1
        elif angle < -TOL_A:
            self.right_wheel_speed = speed * angle_k2
            self.left_wheel_speed = speed * angle_k1

    # this function is simple and may require some tweaking but should work more or less

    # TODO implement some kind of ramping\

    # separate move case for other types of movements
    async def set_motor_speed(self, current_position: Transform, target_position: Transform, rot_right_amount: int,
                              rot_left_amount: int, stop: bool = False, back_slow: bool = False ) -> None:

        angle = current_position.get_rotation_to_target(target_position.get_position())

        #rotated: int = 0 # AC - Did this to stop errors # DM - removed rotated altogether
        if stop:
            self.left_wheel_speed = 0
            self.right_wheel_speed = 0
        if back_slow:
            self.left_wheel_speed = -10 # backup slowly at 10% speed
            self.right_wheel_speed = -10
        if rot_right_amount != 0:
            #DM - fixed - need to get amount needed to rotate in degrees, if we can it would be nice to track the amount weve rotated based off the otis
            #rotated = rotated + 0# amount rotated, cumulative from otos
            if angle <= 2:      # angle is the difference between otos and target angle. 2 provides some room for error
                self.left_wheel_speed = 30
                self.right_wheel_speed = -30
            else :
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0
        if rot_left_amount != 0:
            #DM - fixed - need to get amount needed to rotate in degrees, if we can it would be nice to track the amount weve rotated based off the otis
            #rotated = rotated + 0# amount rotated, cumulative from otis
            if angle <= 2:
                self.left_wheel_speed = -30
                self.right_wheel_speed = 30
            else :
                self.left_wheel_speed = 0
                self.right_wheel_speed = 0




    async def move_forward(self):
        self.left_wheel_speed = 40
        self.right_wheel_speed = 40

    async def move_back(self):
        self.left_wheel_speed = -40
        self.right_wheel_speed = -40

    async def move_back_slower(self):
        self.left_wheel_speed = -35
        self.right_wheel_speed = -35

    async def rotate_right(self):
        self.left_wheel_speed = 40
        self.right_wheel_speed = -40

    async def rotate_left(self):
        self.left_wheel_speed = -40
        self.right_wheel_speed = 40

    async def dont_move(self):
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0

    def set_auger_flag(self, auger_flag: int):
        self.auger_flag = auger_flag

        # auger flag should be set at the start based off start led

    def set_sweeper_flag(self, sweeper_flag: int):
        logger = logging.getLogger("Nano")
        logger.debug(f"Sweeper flag switched: {sweeper_flag}")
        self.sweeper_flag = sweeper_flag

        # sweeper flag should be set at the start based off start led


    def set_beacon_arm_flag(self, beacon_arm_flag: int):
        self.beacon_arm_flag = beacon_arm_flag

        '''
        get in position, will have to come from testing navigation
        set beacon arm flag to high
        await.rover_wait(3) 
        set beacon arm to 0
            call beacon gripper function\
        back up robot
        set beacon arm to -1
        await.rover_wait(3) 

        '''

    def set_beacon_gripper_flag(self, beacon_gripper_flag: int):
        self.beacon_gripper_flag = beacon_gripper_flag

        '''
        set beacon gripper flag to 1
        wait while robot open its hand
        set beacon gripper to 0, no need to touch again
        '''

    def set_gsc_gripper_flag(self, _gsc_gripper_flag: int):
        self.gsc_gripper_flag = 0

        '''
        get in position and slowly back into container
        wait for limit switch flag from arduino
        once limit switch flag, stop robot 
        set gripper flag
        '''
    def close_gsc_gripper(self):
        self.set_gsc_gripper_flag(0)

    def open_gsc_gripper(self):
        self.set_nsc_gripper_flag(0)

    def set_nsc_gripper_flag(self, nsc_gripper_flag: int):
        self.nsc_gripper_flag = nsc_gripper_flag
        '''
        wait until pressure sensor is pressed
        then set flag to 0
        '''
    def close_nsc_gripper(self):
        self.set_nsc_gripper_flag(-1)

    def open_nsc_gripper(self):
        self.set_nsc_gripper_flag(1)

    def set_gsc_leaner_flag(self, gsc_leaner_flag: int):
        self.gsc_leaner_flag = gsc_leaner_flag

        '''
               get in position and slowly back into container
               wait for limit switch flag from arduino
               once limit switch flag, stop robot 
               set gripper flag
               '''

    def set_nsc_leaner_flag(self, nsc_leaner_flag: int):
        self.nsc_leaner_flag = nsc_leaner_flag

        '''
               wait until pressure sensor is pressed
               then set flag to 0
               '''

class InputPacket(SignalEmitter):
    PRESSURE_THRESHOLD = 20
    def __init__(self):
        super().__init__()
        self.sweeper_flag: int = 0
        self.auger_flag: int = 0
        self.gsc_pressure_sensor: float = 0
        self.nsc_pressure_sensor: float = 0
        self.gsc_limit_switch: int = 0
        self.nsc_limit_switch: int = 0
        self.start_led_switch: int = 0

        self.sweeper_flag_changed = self.add_signal("sweeper_flag_changed")
        self.auger_flag_changed = self.add_signal("auger_flag_changed")
        self.gsc_pressure_sensor_changed = self.add_signal("gsc_pressure_sensor_changed")
        self.nsc_pressure_sensor_changed = self.add_signal("nsc_pressure_sensor_changed")
        self.gsc_limit_switch_changed = self.add_signal("gsc_limit_switch_changed")
        self.nsc_limit_switch_changed = self.add_signal("nsc_limit_switch_changed")
        self.start_led_switch_changed = self.add_signal("start_led_switch_changed")

        self.logger = logging.getLogger("Nano")

    def receive_packet(self, packet_list: list):
        if self.sweeper_flag != packet_list[0]:
            self.sweeper_flag = packet_list[0]
            self.sweeper_flag_changed.emit(self.sweeper_flag)

        if self.auger_flag != packet_list[1]:
            self.auger_flag = packet_list[1]
            self.auger_flag_changed.emit(self.auger_flag)

        if self.gsc_pressure_sensor != packet_list[2]:
            self.gsc_pressure_sensor = packet_list[2]
            self.gsc_pressure_sensor_changed.emit(self.gsc_pressure_sensor)

        if self.nsc_pressure_sensor != packet_list[3]:
            self.nsc_pressure_sensor = packet_list[3]
            self.nsc_pressure_sensor_changed.emit(self.nsc_pressure_sensor)

        if self.gsc_limit_switch != packet_list[4]:
            self.gsc_limit_switch = packet_list[4]
            self.gsc_limit_switch_changed.emit(self.gsc_limit_switch)

        if self.nsc_limit_switch != packet_list[5]:
            self.nsc_limit_switch = packet_list[5]
            self.nsc_limit_switch_changed.emit(self.nsc_limit_switch)

        if packet_list[6] == "1":
            self.start_led_switch = packet_list[6]
            self.start_led_switch_changed.emit(1)

    def check_gsc_pressure_sensor(self) -> bool:
        if self.gsc_pressure_sensor >= self.PRESSURE_THRESHOLD:
            return True
        else:
            return False

    def check_nsc_pressure_sensor(self) -> bool:
        if float(self.nsc_pressure_sensor) >= self.PRESSURE_THRESHOLD:
            return True
        else:
            return False

    def check_gsc_limit_switch(self) -> bool:
        if self.gsc_limit_switch == 1 or self.gsc_limit_switch == "1":
            return True
        else:
            return False

    def check_nsc_limit_switch(self) -> bool:
        if self.nsc_limit_switch == 1 or self.nsc_limit_switch == "1":
            return True
        else:
            return False



    """
    nano -> arduino: comma seperated list
     left wheel speed: float -100 - 100,
     right wheel speed: float -100 - 100,
     auger: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     sweeper: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     beacon arm: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     beacon gripper: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     gsc gripper: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     nsc gripper: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     gsc leaner: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     nsc leaner: int -1 (negative direction) 0 (do not rotate) 1 (rotate in positive direction)
     
     
    arduino -> nano: comma separated list
        sweeper current sensor: int 0 (not stalled) 1 (stalled)
        auger current sensor: int 0 (not stalled) 1 (stalled)
        gsc pressure sensor: float 0 (no pressure) - 100 ("full pressure")
        nsc pressure sensor: float 0 (no pressure) - 100 ("full pressure")
        gsc limit switch: int 0 (not pressed) - 1 (pressed)
        nsc limit switch: int 0 (not pressed) - 1 (pressed)
        photoresistors/start LED detectors: int 0 (not detected) - 1 (Detected) 
        
    """