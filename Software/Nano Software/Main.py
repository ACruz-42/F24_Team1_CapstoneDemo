import math
import asyncio
import logging
import sys
import csv
import qwiic_otos
import time
from datetime import datetime
from pathlib import Path
from ArduinoComms import ArduinoCommunicator
from EventHandler import EventHandler
from StateMachine import StateMachine
from Event import Event, EventType
from State import Vector2, Vector3, Transform
from MotorControl import InputPacket, OutputPacket


# TODO: Consider end of game packet needs (Some kind of flag in output_packet?)


class Rover:
    """
    Main program for controlling the rover.
    """
    LOG_DIR = Path.home() / "Desktop" / "Logs"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    POS_LOG_FILE = LOG_DIR / f"robot_path_{timestamp}.csv"
    NANO_LOG_FILE = LOG_DIR / f"main_log_{timestamp}.log"

    PATH_DIR = Path.home() / "Desktop/RobotPath"
    PATH_FILE = PATH_DIR / f"robot_path.csv"

    def __init__(self):
        # Position from OTOS
        self.position = self.get_initial_transform().get_position()  # Current position
        self.rotation = self.get_initial_transform().rotation  # Current rotation in degrees
        self.light_detected = False
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Position from encoder feedback
        self.encoder_transform = self.get_initial_transform().get_vector3()

        # Position from theoretical events
        self.theoretical_transform = self.get_initial_transform().get_vector3()

        self.logger = logging.getLogger("Nano")
        self._set_up_logger()

        # Set up packet
        self.input_packet = InputPacket()
        self.output_packet = OutputPacket()

        # Connect packet signals
        def _on_sweeper_flag_changed(flag):
            return
            # if not self.output_packet.game_started: return
            # self.output_packet.set_sweeper_flag(-1 if flag else 1) # 1 is truth-y (acts as True)
        self.input_packet.sweeper_flag_changed.connect(_on_sweeper_flag_changed)

        def _on_auger_flag_changed(flag):
            return
            # if self.output_packet.game_started: return
            # self.output_packet.set_auger_flag(-1 if flag else 1)
        self.input_packet.auger_flag_changed.connect(_on_auger_flag_changed)

        self.input_packet.start_led_switch_changed.connect(self._on_light_detected)
        self.input_packet.gsc_pressure_sensor_changed.connect(self._on_gsc_pressure_sensor_changed)
        self.input_packet.nsc_pressure_sensor_changed.connect(self._on_nsc_pressure_sensor_changed)
        self.input_packet.gsc_limit_switch_changed.connect(self._on_gsc_limit_switch_changed)
        self.input_packet.nsc_limit_switch_changed.connect(self._on_nsc_limit_switch_changed)

        self.input_packet.gsc_limit_switch_changed.connect(self.log_point_to_csv)



        # Initialize Arduino communication
        if sys.platform.startswith('win'):  # Specifically startswith, because Darwin is mac, and has win in it
            self.arduino_comms = ArduinoCommunicator(port="COM4", output_packet=self.output_packet, baud_rate=115200)
        else:
            self.arduino_comms = ArduinoCommunicator(port="/dev/ttyACM0", output_packet=self.output_packet, baud_rate=115200)
        self.arduino_comms.connect()
        self.arduino_comms.packet_received.connect(self.input_packet.receive_packet)

        self.feedback_pos = self.get_initial_transform().get_vector3()

        # Initialize EventHandler
        self.event_handler = EventHandler(self.arduino_comms, input_packet = self.input_packet,
                                          output_packet=self.output_packet)
        self.event_handler.feedback_received.connect(self._on_feedback_received)
        self.event_handler.event_completed.connect(self._on_event_completed)
        self.event_handler.request_transform.connect(self.poll_OTOS)
        self.event_handler.container_loaded.connect(self._on_container_loaded)
        def _on_output_packet_request(): return self.output_packet
        self.event_handler.request_output_packet.connect(_on_output_packet_request)

        # Initialize StateMachine
        self.state_machine = StateMachine()
        self.state_machine.request_light_detected.connect(self._on_request_light_detected)
        self.state_machine.path_requested.connect(self._on_path_requested)
        self.state_machine.point_marked.connect(self._on_point_marked)
        self.state_machine.reset_tracking.connect(self._on_reset_Track)
        self.state_machine.current_transform_requested.connect(self.poll_OTOS)

        self.event_handler.move_to_gsc.connect(self.state_machine.pass_move_to_gsc)
        self.event_handler.move_to_nsc.connect(self.state_machine.pass_move_to_nsc)
        self.event_handler.expand_rover.connect(self.state_machine.pass_expand_rover)

        # Initialize OTOS:
        if not sys.platform.startswith('win'):
            self.OTOS = qwiic_otos.QwiicOTOS()
            self._set_up_OTOS()
        else:
            self.OTOS = None

        o_transform = Vector3(self.position.x, self.position.y, self.rotation)
        self.log_position_to_csv(self.theoretical_transform, o_transform, self.encoder_transform)
        self.logger.debug(f"Starting Position - x:{self.encoder_transform.x}, y:{self.encoder_transform.y}, "
                          f"rot:{self.encoder_transform.rot}")
        self.event_handler.current_event_number += 1

        self.testing = False

    def _set_up_logger(self):
        self.logger = logging.getLogger("Nano")
        self.logger.setLevel(logging.DEBUG)

        print_handler = logging.StreamHandler(stream=sys.stdout)
        frmt = logging.Formatter(
            "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s")
        print_handler.setFormatter(frmt)
        print_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.NANO_LOG_FILE)
        file_handler.setFormatter(frmt)
        file_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(print_handler)

        self.logger.info("Nano Logger finished setup.")

    def _set_up_OTOS(self) -> None:
        # if not self.OTOS:  # For debugging,
        #     return
        # Check if it's connected
        if not self.OTOS.is_connected():
            print("The device isn't connected to the system. Please check your connection",
                  file=sys.stderr)
            self.logger.error("OTOS isn't connected to system.")
            return

        # Initialize the device
        self.OTOS.begin()

        # Calibrate the IMU, which removes the accelerometer and gyroscope offsets
        self.OTOS.calibrateImu()

        # Reset the tracking algorithm - this resets the position to the origin,
        # but can also be used to recover from some rare tracking errors
        self.OTOS.resetTracking()

    def _on_reset_Track(self) -> None:
        self.OTOS.resetTracking()

    def _on_feedback_received(self, feedback_string: str):
        feedback_distance = 0
        feedback_angle = 0
        if "rotate" in feedback_string:
            if "right" in feedback_string:
                feedback = feedback_string.split(",")
                feedback_angle = float(feedback[2])
            elif "left" in feedback_string:
                feedback = feedback_string.split(",")
                feedback_angle = -float(feedback[2])
            else:
                self.logger.error(f"Unexpected feedback string: {feedback_string}")
                return
        elif "move" in feedback_string:
            if "forward" in feedback_string:
                feedback = feedback_string.split(",")
                feedback_distance = float(feedback[2])
            elif "back" in feedback_string:
                feedback = feedback_string.split(",")
                feedback_distance = -float(feedback[2])
            else:
                self.logger.error(f"Unexpected feedback string: {feedback_string}")
                return
        else:
            self.logger.error(f"Unexpected feedback string: {feedback_string}")
            return

        if feedback_angle:
            self.encoder_transform.rot = self.clamp_angle(self.encoder_transform.rot + feedback_angle)
        if feedback_distance:
            distance = self.pos_from_distance_and_angle(feedback_distance, self.encoder_transform.rot)
            self.encoder_transform.x += distance.x
            self.encoder_transform.y += distance.y
        self.logger.debug(f"encoder_data - x:{self.encoder_transform.x}, y:{self.encoder_transform.y}, "
                          f"rot:{self.encoder_transform.rot}")

    def _on_event_completed(self, event: Event) -> None:
        """
        Called when an event is completed by the Arduino.
        """

        self.logger.info(f"Rover received event completion: {event}")
        if event.event_type == EventType.MOVE or event.event_type == EventType.ROTATE or event.event_type == \
                EventType.ABSOLUTE_ROTATE:
            self.update_theoretical_position(event)
            self.update_position()

    def _on_container_loaded(self, container: str) -> None:
        match container:
            case "gsc":
                self.logger.debug("GSC loaded")
                self.state_machine.gsc_loaded = True
            case "nsc":
                self.logger.debug("NSC loaded")
                self.state_machine.nsc_loaded = True
            case __:
                self.logger.error(f"Unrecognized _on_container_loaded {container}")

    def _on_light_detected(self, flag) -> None:
        self.light_detected = flag
        self.output_packet.game_started = True

    def _on_request_light_detected(self) -> bool:
        return self.light_detected

    def _on_landing_zone_position_found(self, new_position: int) -> None:
        self.landing_zone_position = new_position

    def _on_landing_zone_position_requested(self) -> int:
        return self.landing_zone_position

    def _on_path_requested(self) -> list:
        return self.read_path_from_csv(self.PATH_FILE)

    def _on_point_marked(self) -> None:
        self.log_point_to_csv(self.PATH_FILE)

    def get_rover_transform(self) -> Transform:
        return Transform(Vector3(self.position.x, self.position.y, self.rotation))

    def _on_gsc_pressure_sensor_changed(self, pressure) -> None:
        self.input_packet.gsc_pressure_sensor = pressure

    def _on_nsc_pressure_sensor_changed(self, pressure) -> None:
        self.input_packet.nsc_pressure_sensor = pressure

    def _on_gsc_limit_switch_changed(self, pressure) -> None:
        self.input_packet.gsc_limit_switch = pressure

    def _on_nsc_limit_switch_changed(self, pressure) -> None:
        self.input_packet.nsc_limit_switch = pressure

    def poll_OTOS(self) -> Transform:
        """
        Returns OTOS' current position converted to internal robot grid
        internal robot grid is clockwise rot
        while OTOS is counterclockwise
        Returns Vector3.
        """
        data = self.OTOS.getPosition()
        self_transform = Transform(Vector3(data.x, data.y, -data.h))
        self_transform.rotation = self.clamp_angle(self_transform.rotation)
        return self_transform

    def update_position(self) -> None:
        """
        Updates the rover's actual position based on OTOS data (and possibly other sensors).
        """
        self.logger.debug("update_position started - ")
        otos_data = self.poll_OTOS()
        otos_data = otos_data.get_vector3()
        self.logger.debug(f"otos_data - x:{otos_data.x}, y:{otos_data.y}, rot:{otos_data.rot}")
        self.position.x = otos_data.x
        self.position.y = otos_data.y
        self.rotation = self.clamp_angle(otos_data.rot)

        self.log_position_to_csv(self.theoretical_transform, otos_data, self.encoder_transform)

    def update_theoretical_position(self, event: Event) -> None:
        """
        Updates the rover's theoretical position based on events.
        """
        self.logger.debug("update_theoretical position -")
        event_data = event.data

        if event.event_type == EventType.MOVE:
            offset_pos = self.pos_from_distance_and_angle(event_data, self.theoretical_transform.rot)
            self.theoretical_transform.x += offset_pos.x
            self.theoretical_transform.y += offset_pos.y
        elif event.event_type == EventType.ROTATE:
            self.theoretical_transform.rot = self.clamp_angle(self.theoretical_transform.rot + event_data)
        self.logger.debug(f"theoretical_transform - x:{self.theoretical_transform.x}, "
                          f"y:{self.theoretical_transform.y}, rot:{self.theoretical_transform.rot}")

    def process_transform(self, transform: Transform) -> None:
        if not transform.position == Vector2.ZERO():
            position_event = Event(EventType.ABSOLUTE_MOVE, transform) if transform.is_absolute() else \
                             Event(EventType.MOVE, transform)
            if transform.rotation == 0:
                position_event.event_finished.connect(transform.position_reached.emit)
            self.event_handler.add_event(position_event)

        if not transform.rotation == 0:
            rotation_event = Event(EventType.ABSOLUTE_ROTATE, transform) if transform.is_absolute() else \
                             Event(EventType.ROTATE, transform)
            rotation_event.event_finished.connect(transform.position_reached.emit)
            self.event_handler.add_event(rotation_event)


    def log_position_to_csv(self, t_transform: Vector3, o_transform: Vector3, e_transform: Vector3):
        """
        Appends the current position and timestamp to a CSV file.
        t_transform = theoretical transform (calculated via internal events)
        o_transform = transform from OTOS (and possibly other sensors)
        e_transform = transform from encoder feedback
        """
        t_transform.rot = round(t_transform.rot, 2)
        write_header = not self.POS_LOG_FILE.exists()
        with open(self.POS_LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["timestamp", "event_number",
                                 "theoretical_x", "theoretical_y",  "theoretical_rot",
                                 "OTOS_x", "OTOS_y", "OTOS_rot",
                                 "encoder_x", "encoder_y", "encoder_rot"])
            writer.writerow([datetime.now().isoformat(), self.event_handler.current_event_number,
                             t_transform.x, t_transform.y, t_transform.rot,
                             o_transform.x, o_transform.y, o_transform.rot,
                            e_transform.x, e_transform.y, e_transform.rot])
        self.logger.info("Position logged.")

    def log_point_to_csv(self, path_file: Path) -> None:
        """
        Logs the current position into a spreadsheet for later recollection and recreation.
        """
        return
        # otos_transform = self.poll_OTOS()
        # with open(self.PATH_FILE, mode='a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([otos_transform.position.x, otos_transform.position.y, otos_transform.rotation])
        # self.logger.info("Position logged.")

    def read_path_from_csv(self, path_file: Path) -> list:
        command_list = []
        with open(path_file, newline='') as file:
            for row in file:
                if len(row) == 2:
                    command_list.append(Vector2(row[0], row[1]))
                if len(row) == 3:
                    command_list.append(Vector3(row[0], row[1], row[2]))
                else:
                    command_list.append(row)
        return command_list

    @staticmethod
    def clamp_angle(angle: float, lower_angle: float = 0, upper_angle: float = 360) -> float:
        while angle < lower_angle:
            angle += 360
        while angle > upper_angle:
            angle -= 360
        return angle

    @staticmethod
    def pos_from_distance_and_angle(distance: int, angle: float) -> Vector2:
        angle_rad = math.radians(angle)             # DM removed + 90 in argument
        x = distance * math.sin(angle_rad)
        y = distance * math.cos(angle_rad)              # DM flipped sin and cos
        offset = Vector2(x, y)
        return offset

    @staticmethod
    def get_initial_transform() -> Transform:
        return Transform(Vector3(0, 0, 0))

    async def run(self, testing=False) -> None:
        """
        Main loop
        """
        if testing:
            self.testing = True
            self.event_handler.testing = True
            self.state_machine.testing = True
            self.event_handler.test_signal.connect(self._on_event_completed)
        # start timer
        self.state_machine.transform_requested.connect(self.event_handler.add_event)
        try:
            event_task = asyncio.create_task(self.event_handler.start())
            state_task = asyncio.create_task(self.state_machine.start())
            # Wait for both tasks to complete (they won't unless canceled)
            await asyncio.gather(event_task, state_task)
        except KeyboardInterrupt:
            self.logger.info("Stopping rover...")
            self.arduino_comms.disconnect()


if __name__ == "__main__":
    time.sleep(20)
    rover = Rover()
    # Start the rover
    asyncio.run(rover.run())
