import serial
import time
import queue
import threading
import sys
from typing import Optional, List
from Event import EventType
from datetime import datetime
from pathlib import Path
from Signal import *


class ArduinoCommunicator(SignalEmitter):
    """
    Handles serial communication with an Arduino, including sending and receiving messages.
    """
    LOG_DIR = Path.home() / "Desktop" / "Logs"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ARDUINO_LOG_FILE = LOG_DIR / f"arduino_log_{timestamp}.log"

    def __init__(self, port: str, baud_rate: int = 9600):
        SignalEmitter.__init__(self)
        self.arduino_logger = None
        self._set_up_logger()
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.message_queue = queue.Queue()  # Queue to store incoming messages
        self.running = False
        self.read_thread = None
        self.waiting = False
        self.stopped = self.add_signal("stopped")
        self.light_detected = self.add_signal("light_detected")
        self.ready_for_command = True

    def _set_up_logger(self):
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

        self.arduino_logger = logging.getLogger("Arduino:")
        self.arduino_logger.setLevel(logging.DEBUG)

        print_handler = logging.StreamHandler(stream=sys.stdout)
        frmt = logging.Formatter(
            "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s")
        print_handler.setFormatter(frmt)
        print_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.ARDUINO_LOG_FILE)
        file_handler.setFormatter(frmt)
        file_handler.setLevel(logging.DEBUG)

        self.arduino_logger.addHandler(file_handler)
        self.arduino_logger.addHandler(print_handler)

        self.arduino_logger.debug("Arduino Logger finished setup.")

    def connect(self):
        """
        Open the serial connection to the Arduino and start the message reading thread.
        """
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            self.arduino_logger.debug(f"Connected to Arduino on {self.port}")

            # Start the message reading thread
            self.running = True
            self.read_thread = threading.Thread(target=self._read_messages)
            self.read_thread.start()
        except Exception as e:
            self.arduino_logger.error(f"Failed to connect to Arduino: {e}")

    def disconnect(self):
        """
        Close the serial connection and stop the message reading thread.
        """
        self.running = False
        if self.read_thread:
            self.read_thread.join()  # Wait for the thread to finish
        if self.ser is None or not self.ser.is_open:
            self.ser.close()
            self.arduino_logger.debug("Disconnected from Arduino.")

    def _read_messages(self):
        """
        Continuously read messages from the Arduino and add them to the message queue.
        """
        while self.running:
            if self.ser and self.ser.is_open:
                response = None
                try:
                    response = self.ser.readline().decode().strip()  # Read response
                    if response:
                        if "debug" in response:
                            self.arduino_logger.debug(f"Debug - Read from Arduino: {response}")
                        elif "error" in response:
                            self.arduino_logger.error(f"Error - Read from Arduino: {response}")
                        elif "stop" in response:
                            self.arduino_logger.debug(f"Stop - Read from Arduino: {response}")
                            self.stopped.emit()
                            self.ready_for_command = True
                        elif "event_completed" in response:
                            self.arduino_logger.debug(f"Event_Completed - Read from Arduino: {response}")
                            self.message_queue.put(response)  # Add message to queue
                        elif "event_failed" in response:
                            self.arduino_logger.error("Event failed - Read from Arduino:")
                            self.message_queue.put(response)
                        elif "light" in response:
                            self.light_detected.emit()
                        else:
                            self.arduino_logger.warning(f"Unknown - Arduino message not recognized: {response}")
                except Exception as e:
                    if response:
                        self.arduino_logger.error(f"Cause of error: {response}")
                    self.arduino_logger.error(f"Error reading from Arduino: {e}")
            else:
                time.sleep(0.1)  # Sleep if the serial connection is not open

    def send_message(self, message: str, wait_for_completion=False) -> Optional[str]:
        """
        Send a message to the Arduino.
        If wait_for_completion is True, wait until an "event_completed" response is received.
        """
        time.sleep(0.1)
        while not self.ready_for_command:
            time.sleep(0.1)
        self.ready_for_command = False
        if  self.ser is None or not self.ser.is_open:
            self.arduino_logger.error("Serial connection not open.")
            return None

        try:
            self.ser.write((message + '\n').encode())  # Send message
            self.arduino_logger.debug(f"Sent to Arduino: {message}")

            if wait_for_completion:
                # Wait for the "event_completed" response
                self.waiting = True
                completion_response = None
                timeout = time.time() + 30  # 30 second timeout

                # Create a temporary queue for messages we process while waiting
                temp_queue = queue.Queue()

                while time.time() < timeout and not completion_response:
                    try:
                        # Use get_nowait() to avoid blocking
                        if not self.message_queue.empty():
                            response = self.message_queue.get_nowait()
                            print("Got response: ", response)
                            if "event_completed" in response:
                                self.arduino_logger.debug(f"event_completed parsed in main thread: {response}")
                                completion_response = response
                            elif "event_failed" in response:
                                self.arduino_logger.error(f"event_failed parsed in main thread: {response}")
                                completion_response = response
                            else:
                                # If not the completion message, store it to put back later
                                temp_queue.put(response)
                        else:
                            # No messages, sleep a bit
                            time.sleep(0.1)
                    except queue.Empty:
                        # Queue was empty, sleep a bit
                        time.sleep(0.1)

                # Put back any messages we processed that weren't the completion message
                while not temp_queue.empty():
                    self.message_queue.put(temp_queue.get())  # TODO: empty queue at some point

                self.waiting = False

                if completion_response:
                    return completion_response
                else:
                    self.arduino_logger.warning(f"Timeout waiting for event_completed")
                    return None

            return message
        except Exception as e:
            self.arduino_logger.error(f"Error sending message: {e}")
            self.waiting = False
            return None

    def send_event(self, event, wait_for_response=True) -> Optional[str]:
        """
        Send an event to the Arduino as a serial message.
        """
        #self.arduino_logger.debug(f"sending event: {str(event)}")
        if self.waiting:
            self.arduino_logger.warning("Already waiting for a response, cannot send another event")
            return None

        if event.event_type == EventType.TRANSFORM:  # TODO: add logging, this should not happen
            self.arduino_logger.warning("Transform event passed through EventHandler unexpectedly.")
            return None
        elif event.event_type == EventType.MOVE:
            if event.data > 0:
                message = f"move_forward,{abs(event.data)}"
            else:
                message = f"move_back,{abs(event.data)}"
        elif event.event_type == EventType.ABSOLUTE_MOVE:
            pass
        elif event.event_type == EventType.ROTATE:
            if event.data > 0:
                message = f"rotate_right,{event.data}"
            else:
                message = f"rotate_left,{abs(event.data)}"
        elif event.event_type == EventType.MANEUVER:
            pass  # This might be a thing in the future, but is not right now.
        elif event.event_type == EventType.LOAD:
            if event.data == 0:
                message = f"GSC_load,"
            elif event.data == 1:
                message = f"NSC_load,"
        elif event.event_type == EventType.EXPAND:
            message = f"expand_robot,"
        elif event.event_type == EventType.BEACON:
            message = f"Beacon,"
        elif event.event_Type == EventType.POLAR:
            message = f"Polar,{event.data},{event.angle}"
        elif event.event_type == EventType.CUSTOM:
            message = f"custom,"
        else:
            self.arduino_logger.error(f"Unknown event type: {event.event_type}")
            return None

        event.mark_finished()
        return self.send_message(message, wait_for_completion=wait_for_response)

    def get_messages(self) -> List[str]:
        """
        Retrieve all messages from the message queue.
        """
        messages = []
        while not self.message_queue.empty():
            messages.append(self.message_queue.get())
        return messages

    async def test(self):
        while True:
            self._read_messages()


if __name__ == "__main__":
    arduino_comms = ArduinoCommunicator(port="COM5", baud_rate=115200)
    arduino_comms.connect()
    asyncio.run(arduino_comms.test())
