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
    CONTROL_LOOP_DURATION = 0.1

    def __init__(self, output_packet, port: str, baud_rate: int = 9600):
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
        self.packet_received = self.add_signal("packet_received")
        self.ready_for_command = True
        self.output_packet = output_packet

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
            time.sleep(1)  # Wait for Arduino to initialize
            self.arduino_logger.debug(f"Connected to Arduino on {self.port}")

            # Start the message reading thread
            self.running = True
            self.read_thread = threading.Thread(target=self.run_control_loop)
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

    def run_control_loop(self):
        while True:
            self.ser.write(str(self.output_packet).encode())
            self.arduino_logger.debug(f"Output packet: {str(self.output_packet)}")
            self.ser.flush()
            response = self.ser.readline().decode().strip()
            if response:
                if "debug" in response:
                    self.arduino_logger.debug(response)
                    return
                serialized_packet = response.split(",")
                if len(serialized_packet) == 7:
                    self.arduino_logger.debug(f"Packet received: {response}")
                    self.packet_received.emit(serialized_packet)
                else:
                    self.arduino_logger.warning(f"Message not recognized: {response}")


    async def control_loop(self) -> None:
        event_task = asyncio.create_task(self._read_packet())
        state_task = asyncio.create_task(self._send_packet())
        # Wait for both tasks to complete (they won't unless canceled)
        await asyncio.gather(event_task, state_task)


    async def _read_packet(self) -> None:
        while True:
            if self.ser and self.ser.is_open:
                response = self.ser.readline().decode().strip()  # Read response
                if response:
                    if "debug" in response:
                        self.arduino_logger.debug(response)
                        return
                    serialized_packet = response.split(",")
                    if len(serialized_packet) == 7:
                        self.arduino_logger.debug(f"Packet received: {response}")
                        self.packet_received.emit(serialized_packet)
                    else:
                        self.arduino_logger.warning(f"Message not recognized: {response}")
            else:
                await asyncio.sleep(0.01)  # Sleep if the serial connection is not open

    async def _send_packet(self) -> None:
        if self.ser is None or not self.ser.is_open:
            self.arduino_logger.error("Serial connection not open.")
            return

        while True:
            self.ser.write((str(self.output_packet) + '\n').encode())  # Send message
            self.arduino_logger.debug(f"Sent to Arduino: {str(self.output_packet)}")
            await asyncio.sleep(0.1)


    def send_message(self, message: str, wait_for_completion=False) -> Optional[str]:
        """
        Send a message to the Arduino.
        If wait_for_completion is True, wait until an "event_completed" response is received.
        """
        if self.ser is None or not self.ser.is_open:
            self.arduino_logger.error("Serial connection not open.")
            return None

        try:
            self.ser.write((message + '\n').encode())  # Send message
            self.arduino_logger.debug(f"Sent to Arduino: {message}")
            return message

        except Exception as e:
            self.arduino_logger.error(f"Error sending message: {e}")
            return None

    def send_packet(self, packet) -> None:
        self.send_message(str(packet))



if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyACM0",baudrate=115200,timeout=1)
    print(ser)

    # while True:
    #     packet = "30,30,0,0,0,0,0,0,0,0\n"
    #     ser.write(packet.encode())
    #     ser.flush()
    #     response = ser.readline().decode().strip()
