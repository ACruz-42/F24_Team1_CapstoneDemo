import queue
import time
import math
from MotorControl import InputPacket, OutputPacket
from ArduinoComms import ArduinoCommunicator
from Event import *
from State import Vector2, Vector3, Transform

CONTROL_LOOP_DURATION = 0.1
ROTATION_OFFSET_THRESHOLD = 10


class EventHandler(SignalEmitter):
    """
    Handles a queue of events and sends them to the Arduino.
    """
    def __init__(self, arduino_comms: ArduinoCommunicator, input_packet:InputPacket, output_packet:OutputPacket):
        SignalEmitter.__init__(self)
        self.event_queue = queue.Queue()  # Queue to hold events
        self.arduino_comms = arduino_comms  # Arduino communication handler
        self.running = False
        self.logger = None
        self.event_completed = self.add_signal("event_completed")
        self.request_transform = self.add_signal("request_transform")
        self.feedback_received = self.add_signal("feedback_received")
        self.container_loaded = self.add_signal("contained_loaded")
        self.request_output_packet = self.add_signal("request_output_packet")
        self.move_to_gsc = self.add_signal("move_to_gsc")
        self.move_to_nsc = self.add_signal("move_to_nsc")
        self.expand_rover = self.add_signal("expand_rover")
        self.current_event_number = 0

        self.input_packet = input_packet
        self.output_packet = output_packet

        self.testing = False
        self.test_signal = self.add_signal("testing")

    def add_event(self, event: Event):
        """
        Add an event to the queue.
        """
        self.event_queue.put(event)
        self.logger.info(f"Added event to queue: {event}")

    def clear_queue(self) -> None:
        with self.event_queue.mutex:
                self.event_queue.queue.clear()

    async def process_event(self, event: Event):
        """
        Process a single event and send it to the Arduino.
        """
        await self._ensure_connection_open()
        self.logger.debug(f"Processing event of type: {event.event_type}")
        match event.event_type:
            case EventType.MOVE:
                await self._handle_move_event(event)
            case EventType.PRECISE_MOVE:
                await self._handle_precise_move_event(event)
            case EventType.RELATIVE_MOVE:
                await self._handle_relative_move_event(event)
            case EventType.ROTATE:
                await self._handle_rotate_event(event)
            case EventType.EXPAND:
                await self._handle_expand_event(event)
            case EventType.LOAD:
                if event.data == 0:  # A slight hack for convenience's sake 0 = gsc, 1 = nsc
                    await self._handle_load_gsc_event(event)
                elif event.data == 1:
                    await self._handle_load_nsc_event(event)
            case EventType.BEACON:
                await self._handle_beacon_event(event)
            case EventType.RETRACT:
                await self._handle_retract_event(event)
            case __:
                self.logger.warning(f"Unhandled event type: {event.event_type}")

    async def _ensure_connection_open(self):
        """Ensure Arduino communication is open before proceeding."""
        while not self.arduino_comms.ser.is_open:
            self.logger.warning("Comms not open")
            await asyncio.sleep(1)

    async def _handle_move_event(self, event: Event):
        """Handle direct move events."""
        target_position = event.data
        self.logger.debug(f"Handling move event with target_position: {target_position}")

        await self._move_to(target_position)  # This is related to  AsyncIO
        self.logger.info(f"Move event_completed: {event}")

        event.mark_finished()

    async def _handle_precise_move_event(self, event: Event):
        """Handle direct move events."""
        target_position = event.data
        self.logger.debug(f"Handling precise move event with target_position: {target_position}")

        await self._precise_move_to(target_position)  # This is related to  AsyncIO
        self.logger.info(f"Precise move event_completed: {event}")

        event.mark_finished()

    async def _handle_relative_move_event(self, event: Event):
        duration = event.data
        self.logger.debug(f"Handling relative move event with duration: {duration}")

        if duration > 0:
            await self.output_packet.move_forward()
            await asyncio.sleep(duration)
            await self.output_packet.dont_move()
        if duration < 0:
            await self.output_packet.move_back()
            duration = abs(duration)
            await asyncio.sleep(duration)
            await self.output_packet.dont_move()

            event.mark_finished()

    async def _handle_rotate_event(self, event: Event):
        """Handle direct rotate events."""
        target_rotation = event.data
        self.logger.debug(f"Handling rotation event with target_rotation: {target_rotation}")
        try:
            await self._rotate_to(target_rotation)  # This is related to  AsyncIO
            self.logger.info(f"Rotate event_completed: {event}")

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during rotation: {e}")


    async def _handle_expand_event(self, event: Event):
        self.logger.debug(f"Handling expand event.")

        try:
            self.output_packet.set_nsc_gripper_flag(1) # Check this flag
            self.output_packet.set_gsc_gripper_flag(1)
            await asyncio.sleep(4)
            self.output_packet.set_nsc_gripper_flag(0)
            self.output_packet.set_gsc_gripper_flag(0)
            self.logger.info(f"Expand event_completed")
            # turn on auger and sweeper, move back nsc (leaner)

            self.output_packet.set_sweeper_flag(-1)
            await asyncio.sleep(1)
            self.output_packet.set_sweeper_flag(1)
            self.output_packet.set_auger_flag(-1)
            self.output_packet.set_auger_flag(1)
            self.output_packet.set_nsc_leaner_flag(1)

            self.event_completed.emit(event)
            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during expand event: {e}")

    async def _handle_retract_event(self, event: Event):
        self.logger.debug(f"Handling retract event.")

        try:
            self.output_packet.set_nsc_gripper_flag(-1) # Check this flag
            self.output_packet.set_gsc_gripper_flag(-1)
            await asyncio.sleep(15)
            self.output_packet.set_nsc_gripper_flag(0)
            self.output_packet.set_gsc_gripper_flag(0)
            self.logger.info(f"Retract event_completed")

            self.event_completed.emit(event)
            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during retract event: {e}")

    async def _handle_load_gsc_event(self, event: Event):
        self.logger.debug(f"Handling load Geodinium SC event.")

        try:
            await self._handle_gsc_load()
            self.event_completed.emit(event)
            event.mark_finished()

        except Exception as e:
            self.logger.error(f"Error during GSC load event: {e}")

    async def _handle_load_nsc_event(self, event: Event):
        self.logger.debug(f"Handling load Nebulite SC event.")

        try:
            await self._handle_nsc_load()
            self.event_completed.emit(event)
            event.mark_finished()

        except Exception as e:
            self.logger.error(f"Error during NSC load event: {e}")

    async def _handle_beacon_event(self, event: Event):
        self.logger.debug(f"Handling beacon event.")

        try:
            await self._handle_beacon()
            self.logger.info(f"Beacon event_completed: {event}")
            self.event_completed.emit(event)
            event.mark_finished()

        except Exception as e:
            self.logger.error(f"Error during expand event: {e}")

    async def _handle_beacon(self):
        """
        Used for beacons.
        """
        time_elapsed = 0
        while time_elapsed <= 1:
            self.output_packet.set_beacon_arm_flag(-1)
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION

        time_elapsed = 0
        while time_elapsed <= 2.5:
            self.output_packet.set_beacon_gripper_flag(-1)
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION

        await self.output_packet.move_back()
        time_elapsed = 0
        while time_elapsed <= 0.5:
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION
        await self.output_packet.dont_move()

        time_elapsed = 0
        while time_elapsed <= 1:
            self.output_packet.set_beacon_arm_flag(1)
            self.output_packet.set_beacon_gripper_flag(1)
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION

    async def _handle_gsc_load(self, time_elapsed = 0) -> None:
        if time_elapsed > 25:
            return
        timeout = 5
        # Let's assume we're in the right "ready position", the position and rotation to back up
        # set packet to slowly back up
        await self.output_packet.move_back()

        # wait for limit switch to activate
        while (not self.input_packet.check_gsc_limit_switch()) or time_elapsed > timeout:
            self.logger.debug("inside loop")
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION

        await self.output_packet.dont_move()

        if time_elapsed > timeout and not self.input_packet.check_gsc_limit_switch():
            self.move_to_gsc.emit()
            await self._handle_gsc_load(time_elapsed)
            return

        time_elapsed = 0
        self.output_packet.close_gsc_gripper()
        grabbed_flag = True

        for idx in range(4):
            if grabbed_flag:
                while not (self.input_packet.check_gsc_pressure_sensor() or time_elapsed > timeout):
                    if time_elapsed > timeout:
                        grabbed_flag = False
                        break
                    else:
                        self.output_packet.close_gsc_gripper()
                    await asyncio.sleep(CONTROL_LOOP_DURATION)
                    time_elapsed += CONTROL_LOOP_DURATION
            else:
                self.output_packet.open_gsc_gripper()
                await asyncio.sleep(3)
                grabbed_flag = True

        if not grabbed_flag:
            return

    async def _handle_nsc_load(self, time_elapsed=0) -> None:
        if time_elapsed > 25:
            return
        # if time_elapsed > 5:
        #     inter_timer = time_elapsed % 5      # used to keep check of time between recursive calls
        # else:
        #     inter_timer = 0
        timeout = 5
        # Let's assume we're in the right "ready position", the position and rotation to back up
        # set packet to slowly back up
        await self.output_packet.move_back_slower()

        # wait for limit switch to activate
        while (time_elapsed < timeout):# self.input_packet.check_nsc_limit_switch() or inter_timer > timeout):
            self.logger.debug(f"time elapsed:{time_elapsed}")
            await asyncio.sleep(CONTROL_LOOP_DURATION)
            time_elapsed += CONTROL_LOOP_DURATION

        await self.output_packet.dont_move()

        for idx in range(4):
            if not (self.input_packet.check_nsc_pressure_sensor() == "1" or self.input_packet.check_nsc_pressure_sensor() == 1):
                #await self.output_packet.move_forward()
                await asyncio.sleep(0.5)
                #await self.output_packet.move_back()
                await asyncio.sleep(1)

        self.output_packet.close_nsc_gripper()
        self.output_packet.set_nsc_leaner_flag(1)

        # if inter_timer > timeout and not self.input_packet.check_nsc_limit_switch():
        #     self.move_to_nsc.emit()
        #     await self._handle_nsc_load(time_elapsed)
        #     return
        #
        # #time_elapsed = 0
        # self.output_packet.close_nsc_gripper()
        # grabbed_flag = True
        #
        # for idx in range(4):
        #     if grabbed_flag:
        #         while not (self.input_packet.check_nsc_pressure_sensor() or time_elapsed > timeout):
        #             if time_elapsed > timeout:
        #                 grabbed_flag = False
        #                 break
        #             else:
        #                 self.output_packet.close_nsc_gripper()
        #             await asyncio.sleep(CONTROL_LOOP_DURATION)
        #             time_elapsed += CONTROL_LOOP_DURATION
        #     else:
        #         self.output_packet.open_nsc_gripper()
        #         await asyncio.sleep(3)
        #         grabbed_flag = True
        #
        # if not grabbed_flag:
        #     return
        # self.output_packet.set_nsc_leaner_flag(-1)

    async def _rotate_to(self, target_rotation) -> None:
        self.logger.debug("Rotate to - ")
        self.logger.debug(f"targert_rotation: {target_rotation}")
        current_transform: Transform = self.request_transform.emit()[0]
        self.logger.debug(f"current transform: {current_transform}")
        closest_direction =  current_transform.get_shortest_rotation_to(target_rotation)
        if closest_direction == 0:
            return
        self.logger.debug(f"closest direction: {closest_direction}")
        if closest_direction > 0:
            self.logger.debug(f"closest direction is right")
            await self.output_packet.rotate_right()
        else:
            self.logger.debug(f"closest direction is left")
            await self.output_packet.rotate_left()

        while not self._rot_is_close_enough(self.request_transform.emit()[0].rotation, target_rotation):
            pass # NOTE: we can change this to update motor speeds if necessary, using offset

        await self.output_packet.dont_move()

    async def _move_to(self, target_position: Transform) -> None:
        self.logger.debug("Move to -")
        current_transform: Transform = self.request_transform.emit()[0]
        self.logger.debug(f"current transform: {current_transform}")

        await self.output_packet.move_forward()

        def reached_or_overshot_target(starting: Transform, current: Transform, target: Transform):
            distance = starting.position.distance_to(target.position)
            distance *= 1.2
            travelled_distance = starting.position.distance_to(current.position)
            if self._pos_is_close_enough(current, target):
                return True
            elif travelled_distance > distance:
                return True
            else:
                return False

        while not reached_or_overshot_target(current_transform, self.request_transform.emit()[0], target_position):
            new_position = self.request_transform.emit()[0]
            rotation_to_target = new_position.get_rotation_to_target(target_position.get_position())
            if abs(new_position.rotation - rotation_to_target) > ROTATION_OFFSET_THRESHOLD:
                await self._rotate_to(rotation_to_target)
            else:
                await self.output_packet.move_forward() # NOTE: we can change this to update the motor speeds if necessary

        await self.output_packet.dont_move()


    async def _precise_move_to(self, target_position: Transform) -> None:
        self.logger.debug("Move to -")
        current_transform: Transform = self.request_transform.emit()[0]
        self.logger.debug(f"current transform: {current_transform}")

        await self.output_packet.move_forward()

        def reached_or_overshot_target(starting: Transform, current: Transform, target: Transform):
            distance = starting.position.distance_to(target.position)
            distance *= 1.05
            travelled_distance = starting.position.distance_to(current.position)
            if self._pos_is_close_enough(current, target, 1.2):
                return True
            elif travelled_distance > distance:
                return True
            else:
                return False

        while not reached_or_overshot_target(current_transform, self.request_transform.emit()[0], target_position):
            new_position = self.request_transform.emit()[0]
            rotation_to_target = new_position.get_rotation_to_target(target_position.get_position())
            if abs(new_position.rotation - rotation_to_target) > ROTATION_OFFSET_THRESHOLD:
                await self._rotate_to(rotation_to_target)
            else:
                await self.output_packet.move_forward()  # NOTE: we can change this to update the motor speeds if necessary

        await self.output_packet.dont_move()


    async def start(self):
        """
        Start processing events from the queue.
        """
        self.running = True
        self.logger = logging.getLogger("Nano")
        self.logger.info("Event Handler started ")
        while self.running:
            if not self.event_queue.empty():
                self.logger.debug("running")
                event = self.event_queue.get()
                await self.process_event(event)
            else:
                #self.logger.debug("not running")
                await asyncio.sleep(0.05)  # Sleep to avoid busy-waiting

    def stop(self):
        """
        Stop processing events.
        """
        self.running = False
        self.logger.info("Event Handler stopped ")

    def _calculate_target_position(self, transform_data, current_pos):
        """Calculate the target position based on whether it's absolute or relative."""
        if transform_data.is_absolute():
            self.logger.debug("Using absolute position.")
            return transform_data
        else:
            self.logger.info(f"Process_Event started: relative transformation")
            self.logger.debug(f"Transform data: {transform_data}")
            self.logger.debug(f"Current position: {current_pos}")

            target_pos = Transform(Vector3(
                transform_data.position.x + current_pos.position.x,
                transform_data.position.y + current_pos.position.y,
                0
            ))
            self.logger.debug(f"Target position: {target_pos}")
            return target_pos

    @staticmethod
    def _should_move_backwards(transform_data):
        """Determine if movement should be backwards based on transform data."""
        # This makes the assumption that if the transform_data is negative, we want to move backwards.
        return transform_data.position.x < 0 or transform_data.position.y < 0

    @staticmethod
    def _pos_is_close_enough(current_pos: Transform, target_pos: Transform, close_enough_distance=2.0):
        if current_pos.position.distance_to(target_pos.position) <= close_enough_distance:
            return True
        else:
            return False

    @staticmethod
    def _rot_is_close_enough(current_rot, target_rot, close_enough_rotation=5.0):
        target_rotation_plus = target_rot + 360
        target_rotation_minus = target_rot - 360
        if abs(current_rot-target_rot) <= close_enough_rotation:
            return True
        elif abs(current_rot-target_rotation_plus) <= close_enough_rotation:
            return True
        elif abs(current_rot-target_rotation_minus) <= close_enough_rotation:
            return True
        else:
            return False

    @staticmethod
    async def test():
        """
        Test functionality of the EventHandler class.
        """
        print("Testing EventHandler...")

        # Create an instance of ArduinoComms
        arduino_comms = ArduinoCommunicator(port="/dev/ttyACM0", baud_rate=115200)
        arduino_comms.connect()

        # Create an instance of EventHandler
        test_event_handler = EventHandler(arduino_comms)

        # Create test events
        test_event1 = Event(EventType.MOVE, {"distance": 10})
        test_event2 = Event(EventType.ROTATE, {"angle": 45})

        # Add events to the queue
        test_event_handler.add_event(test_event1)
        test_event_handler.add_event(test_event2)

        # Start processing events
        await test_event_handler.start()

        # Let it run for a few seconds
        time.sleep(5)

        # Stop the event handler
        test_event_handler.stop()
        arduino_comms.disconnect()


if __name__ == "__main__":
    event_handler = EventHandler
    asyncio.run(event_handler.test)
