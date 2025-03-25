import queue
import time
import math
from ArduinoComms import ArduinoCommunicator
from Event import *
from State import Vector2, Vector3, Transform


class EventHandler(SignalEmitter):
    """
    Handles a queue of events and sends them to the Arduino.
    """
    def __init__(self, arduino_comms: ArduinoCommunicator, testing=False):
        SignalEmitter.__init__(self)
        self.event_queue = queue.Queue()  # Queue to hold events
        self.arduino_comms = arduino_comms  # Arduino communication handler
        self.running = False
        self.add_signal("event_completed")
        self.event_completed = self.add_signal("event_completed")
        self.request_transform = self.add_signal("request_transform")
        self.feedback_received = self.add_signal("feedback_received")
        self.container_loaded = self.add_signal("contained_loaded")
        self.logger = None
        self.current_event_number = 0

        self.testing = testing
        self.test_signal = self.add_signal("testing")

    def add_event(self, event: Event):
        """
        Add an event to the queue.
        """
        self.event_queue.put(event)
        self.logger.info(f"Added event to queue: {event}")

    async def process_event(self, event: Event):
        """
        Process a single event and send it to the Arduino.
        """
        try:
            await self._ensure_connection_open()
            self.logger.debug(f"Processing event of type: {event.event_type}")
            match event.event_type:
                case EventType.TRANSFORM:
                    event.event_number = self.current_event_number
                    await self._handle_transform_event(event)
                case EventType.MOVE:
                    event.event_number = self.current_event_number
                    await self._handle_move_event(event)
                    self.current_event_number += 1
                case EventType.ROTATE:
                    event.event_number = self.current_event_number
                    await self._handle_rotate_event(event)
                    self.current_event_number += 1
                case EventType.ABSOLUTE_ROTATE:
                    event.event_number = self.current_event_number
                    await self._handle_absolute_rotate_event(event)
                    self.current_event_number += 1
                case EventType.EXPAND:
                    await self._handle_expand_event(event)
                case EventType.LOAD:
                    if event.data == 0:
                        await self._handle_load_gsc_event(event)
                    elif event.data == 1:
                        await self._handle_load_nsc_event(event)
                case EventType.FIND_PATH:
                    await self._handle_find_path_event(event)
                case EventType.BEACON:
                    await self._handle_beacon_event(event)
                case EventType.POLAR:
                    await self._handle_polar(event)
                case __:
                    self.logger.warning(f"Unhandled event type: {event.event_type}")

        except Exception as e:
            self.logger.critical(f"Error processing event: {e}")

    async def _ensure_connection_open(self):
        """Ensure Arduino communication is open before proceeding."""
        while not self.arduino_comms.ser.is_open:
            self.logger.warning("Comms not open")
            await asyncio.sleep(1)

    async def _handle_transform_event(self, event: Event):
        """Handle transform events including movement and rotation."""
        moved = False
        current_pos = self.request_transform.emit()[0]

        # Handle position changes if needed
        if event.data.position != Vector2.ZERO():
            self.logger.debug("Event requires translation.")
            target_pos = self._calculate_target_position(event.data, current_pos)

            # Rotate to face the target position
            await self._rotate_to_face_target(target_pos)
            self.current_event_number += 0.25

            # Move to the target position
            moved = await self._move_to_target(target_pos, event.data, event.backwards)
            self.current_event_number += 0.25

        # Handle rotation changes if needed
        if event.data.rotation != 0:
            await self._handle_rotation(event.data, moved)
            self.current_event_number += 0.5

        self.current_event_number = math.ceil(self.current_event_number)

        # Mark the event as finished
        event.mark_finished()  # This is related to  AsyncIO

    async def _handle_move_event(self, event: Event):
        """Handle direct move events."""
        move_amount = event.data
        self.logger.debug(f"Handling direct move event with amount: {move_amount}")

        try:
            self.test_signal.emit(event)
            move_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO
            self.feedback_received.emit(move_response)
            self.logger.info(f"Direct move event_completed: {move_response}")

            if move_response:
                self.event_completed.emit(event)

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during direct movement: {e}")

    async def _handle_rotate_event(self, event: Event):
        """Handle direct rotate events."""
        rotation_amount = event.data
        self.logger.debug(f"Handling direct rotation event with amount: {rotation_amount}")

        try:
            self.test_signal.emit(event)
            rotate_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO
            self.feedback_received.emit(rotate_response)
            self.logger.info(f"Direct rotation event_completed: {rotate_response}")

            if rotate_response:
                self.event_completed.emit(event)

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during direct rotation: {e}")

    async def _handle_absolute_rotate_event(self, event: Event):
        target_rotation = event.data
        self.logger.debug(f"Handling absolute rotation event with target rotation: {target_rotation}")
        current_transform = self.request_transform.emit()[0]
        desired_rotation = current_transform.get_shortest_rotation_to(target_rotation)
        final_event = Event(EventType.ROTATE, desired_rotation)

        try:
            rotate_response = self.arduino_comms.send_event(final_event)
            await final_event.event_finished.wait()
            event.mark_finished()
            self.feedback_received.emit(rotate_response)
            self.logger.info(f"Absolute rotation event event_completed: {rotate_response}")

            if rotate_response:
                self.event_completed.emit(event)

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during direct rotation: {e}")

    async def _handle_expand_event(self, event: Event):
        self.logger.debug(f"Handling expand event.")

        try:
            self.test_signal.emit(event)
            expand_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO
            self.logger.info(f"Expand event_completed: {expand_response}")

            if expand_response:
                self.event_completed.emit(event)
            else:
                self.logger.warning("No expand response received.")

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during expand event: {e}")

    async def _handle_load_gsc_event(self, event: Event):
        self.logger.debug(f"Handling load Geodinium SC event.")

        try:
            self.test_signal.emit(event)
            expand_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO

            if "event_completed" in expand_response:
                self.logger.info(f"Load Geodinium SC event_completed: {expand_response}")
                self.container_loaded.emit("gsc")
                event.event_success = True
            elif "event_failed" in expand_response:
                self.logger.error(f"Load Geodinium SC event_failed: {expand_response}")
            else:
                self.logger.warning(f"Unrecognized expand_response:{expand_response}")

            if expand_response:
                self.event_completed.emit(event)
            else:
                self.logger.warning("No load Geodinium SC response received.")

            event.mark_finished()

        except Exception as e:
            self.logger.error(f"Error during GSC load event: {e}")

    async def _handle_load_nsc_event(self, event: Event):
        self.logger.debug(f"Handling load Nebulite SC event.")

        try:
            self.test_signal.emit(event)
            expand_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO

            if "event_completed" in expand_response:
                self.logger.info(f"Load Nebulite SC event_completed: {expand_response}")
                self.container_loaded.emit("nsc")
                event.event_success = True
            elif "event_failed" in expand_response:
                self.logger.error(f"Load Nebulite SC event_failed: {expand_response}")
            else:
                self.logger.warning(f"Unrecognized expand_response:{expand_response}")

            if expand_response:
                self.event_completed.emit(event)
            else:
                self.logger.warning("No load Nebulite SC response received.")

            event.mark_finished()

        except Exception as e:
            self.logger.error(f"Error during NSC load event: {e}")

    async def _handle_beacon_event(self, event: Event):
        self.logger.debug(f"Handling beacon event.")

        try:
            self.test_signal.emit(event)
            beacon_response = self.arduino_comms.send_event(event)
            await event.event_finished.wait()  # This is related to  AsyncIO
            self.logger.info(f"Beacon event_completed: {beacon_response}")

            if beacon_response:
                self.event_completed.emit(event)
            else:
                self.logger.warning("No beacon response received.")

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during expand event: {e}")

    async def _handle_find_path_event(self, event: Event):
        self.logger.debug(f"Handling find path event.")

        try:
            pass
            # self.test_signal.emit(event)
            # beacon_response = self.arduino_comms.send_event(event)
            # await event.event_finished.wait()  # This is related to  AsyncIO
            # self.logger.info(f"Beacon event_completed: {beacon_response}")
            #
            # if beacon_response:
            #     self.event_completed.emit(event)
            # else:
            #     self.logger.warning("No beacon response received.")

            event.mark_finished()
        except Exception as e:
            self.logger.error(f"Error during find path event: {e}")

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

    async def _rotate_to_face_target(self, target_pos):
        """Rotate to face the target position."""
        current_pos = self.request_transform.emit()[0]
        target_rotation = current_pos.get_rotation_to_target(target_pos.position)
        if target_rotation == 0:
            return

        rotate_amount = current_pos.get_shortest_rotation_to(target_rotation)

        rotate_event = Event(EventType.ROTATE, rotate_amount)
        try:
            if self.testing:
                self.test_signal.emit(rotate_event)
            rotate_response = self.arduino_comms.send_event(rotate_event)
            await rotate_event.event_finished.wait()  # This is related to  AsyncIO
            self.logger.info(f"Intermediate rotate event_completed: {rotate_response}")
            self.feedback_received.emit(rotate_response)

            if rotate_response:
                self.event_completed.emit(rotate_event)
        except Exception as e:
            self.logger.error(f"Error during intermediate rotation: {e}")

    async def _move_to_target(self, target_pos, transform_data, move_backwards=False):
        """Move to the target position."""
        # Recalculate current position after rotation
        current_pos = self.request_transform.emit()[0]
        move_amount = current_pos.position.distance_to(target_pos.position)

        if self._should_move_backwards(transform_data) and move_backwards:
            move_amount *= -1

        self.logger.debug(f"Move amount: {move_amount}")
        if move_amount == 0:
            return False

        move_event = Event(EventType.MOVE, move_amount)
        try:
            self.test_signal.emit(move_event)
            move_response = self.arduino_comms.send_event(move_event)
            await move_event.event_finished.wait()  # This is related to  AsyncIO
            self.feedback_received.emit(move_response)
            self.logger.info(f"Movement event_completed: {move_response}")

            if move_response:
                self.event_completed.emit(move_event)

            return True
        except Exception as e:
            self.logger.error(f"Error during movement: {e}")
            return False

    async def _handle_rotation(self, transform_data, moved):
        """Handle rotation to the target angle."""
        current_pos = self.request_transform.emit()[0]

        if transform_data.is_absolute() or moved:
            target_rot = current_pos.get_shortest_rotation_to(transform_data.rotation)
        else:
            target_rot = transform_data.rotation

        if target_rot == 0:
            return

        rotate_event = Event(EventType.ROTATE, target_rot)
        try:
            self.test_signal.emit(rotate_event)
            rotate_response = self.arduino_comms.send_event(rotate_event)
            await rotate_event.event_finished.wait()  # This is related to  AsyncIO
            self.feedback_received.emit(rotate_response)
            self.logger.info(f"Destination rotate event_completed: {rotate_response}")

            if rotate_response:
                self.event_completed.emit(rotate_event)
        except Exception as e:
            self.logger.error(f"Error during final rotation: {e}")

    async def _handle_polar(self, event):
        current_transform = self.request_transform.emit()[0]
        target_transform = event.data
        while not self._is_close_enough(current_transform, target_transform):
            event.angle = current_transform.get_shortest_rotation_to(target_transform)
            self.arduino_comms.send_event(event)
            await asyncio.sleep(0.1)
        self.event_completed.emit(event)
        event.mark_finished()

    async def start(self):
        """
        Start processing events from the queue.x
        """
        self.running = True
        self.logger = logging.getLogger("Nano")
        self.logger.info("Event Handler started ")
        while self.running:
            if not self.event_queue.empty():
                event = self.event_queue.get()
                await self.process_event(event)
            else:
                await asyncio.sleep(0.5)  # Sleep to avoid busy-waiting

    def stop(self):
        """
        Stop processing events.
        """
        self.running = False
        self.logger.info("Event Handler stopped ")

    @staticmethod
    def _should_move_backwards(transform_data):
        """Determine if movement should be backwards based on transform data."""
        # This makes the assumption that if the transform_data is negative, we want to move backwards.
        return transform_data.position.x < 0 or transform_data.position.y < 0

    @staticmethod
    def _is_close_enough(current_pos, target_pos, close_enough_distance=1):
        if current_pos.position.distance_to(target_pos) <= close_enough_distance:
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
