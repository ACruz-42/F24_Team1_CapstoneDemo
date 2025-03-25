from enum import Enum
from Signal import *


# Define types of events
class EventType(Enum):
    TRANSFORM = "transform"
    MOVE = "move"
    ABSOLUTE_MOVE = "absolute_move"
    ROTATE = "rotate"
    ABSOLUTE_ROTATE = "absolute_rotate"
    MANEUVER = "maneuver"
    EXPAND = "expand"
    LOAD = "load"
    FIND_PATH = "find_path"
    BEACON = "beacon"
    CUSTOM = "custom"


class Event(SignalEmitter):
    """
    Represents an event with a type and associated data.
    """

    def __init__(self,  event_type: EventType, data):
        SignalEmitter.__init__(self)
        self.event_type = event_type
        self.data = data
        self.event_finished = asyncio.Event()
        self.event_success = False # This is exclusively used for the loading events
        self.event_number = -1
        self.backwards = False

    def __str__(self):
        return f"Event(type={self.event_type}, data={self.data})"

    def mark_finished(self):
        """Mark this event as finished, triggering any waiters."""
        self.event_finished.set()
