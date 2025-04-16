from typing import List
from RoverStates import *
import asyncio
import time
from datetime import datetime
class StateMachine(SignalEmitter):
    def __init__(self):
        SignalEmitter.__init__(self)
        self.logger = None
        self.transform_requested = self.add_signal("transform_requested")
        self.current_transform_requested = self.add_signal("current_transform_requested")
        self.request_light_detected = self.add_signal("request_light_detected")
        self.request_emergency_exit = self.add_signal("request_emergency_exit")
        self.path_requested = self.add_signal("request_path")
        self.point_marked = self.add_signal("point_marked")
        self.reset_tracking = self.add_signal("reset_tracking")
        self.current_state: State | None = None
        self.current_index: int = 0
        self.starting_time = time.time()
        # self.state_list: List = [WaitState, SenseState, BeaconState, GCSCState, NCSCState, CavePrepState,
        #                              CaveVacuumState, MaterialPickupState]
        self.state_list: List = [ShowcaseState]

        self.nsc_loaded = False
        self.gsc_loaded = False
        self.expanded = False
        self.loading_zone = -1

        self.testing = False  # Intended for testing purposes, do not set to True

    async def start(self):
        """
        Starts the state machine.
        """
        self.logger = logging.getLogger("Nano")
        self.logger.info("State Machine started ")
        if self.state_list:
            self.current_state = self.state_list[self.current_index]()
            async def transition_to_next(): await self.transition_to(self.current_index + 1)
            self.current_state.done.connect(transition_to_next)
            self.current_state.transform_request.connect(self.transform_requested.emit)
            self.current_state.request_light_detected.connect(self.request_light_detected.emit)
            self.current_state.april_tag_found.connect(self._on_april_tag_found)
            self.current_state.reset_tracking.connect(self.reset_tracking.emit)
            self.current_state.request_current_transform.connect(self.current_transform_requested.emit)
            self.current_state.starting_time = self.starting_time
            await self.current_state.enter()

    async def transition_to(self, index: int):
        """
        Transitions to the next state.
        """
        if index >= len(self.state_list):
            return

        if self.current_state:
            self.current_state.done.disconnect_all()
            self.current_state.transform_request.disconnect_all()
            self.current_state.request_light_detected.disconnect_all()
            self.current_state.april_tag_found.disconnect_all()
            self.current_state.request_loading_zone.disconnect_all()
            self.current_state.request_emergency_exit.disconnect_all()
            self.current_state.mark_point.disconnect_all()
            self.current_state.request_path.disconnect_all()
            self.current_state.request_current_transform.disconnect_all()
            await self.current_state.exit()

        self.current_index = index
        self.current_state = self.state_list[index]()
        async def transition_to_next(): await self.transition_to(self.current_index + 1)
        self.current_state.done.connect(transition_to_next)
        self.current_state.transform_request.connect(self.transform_requested.emit)
        self.current_state.april_tag_found.connect(self._on_april_tag_found)
        self.current_state.request_loading_zone.connect(self._on_loading_zone_requested)
        self.current_state.request_emergency_exit.connect(self.request_emergency_exit.emit)
        self.current_state.mark_point.connect(self.point_marked.emit)
        self.current_state.request_path.connect(self.path_requested.emit)
        self.current_state.request_current_transform.connect(self.current_transform_requested.emit)
        self.current_state.starting_time = self.starting_time


        await self.current_state.enter()

    async def pass_move_to_gsc(self):
        await self.current_state.move_to_gsc()

    async def pass_move_to_nsc(self):
        await self.current_state.move_to_nsc()

    async def pass_expand_rover(self):
        await self.current_state.expand_rover()

    async def _on_april_tag_found(self, tag_number: int) -> None:
        self.loading_zone = tag_number

    async def _on_loading_zone_requested(self) -> Vector3:
        match self.loading_zone:
            case 0:
                return Vector3(0,0,0)
            case 1:
                return Vector3(0,0,0)
            case 2:
                return Vector3(0,0,0)
            case 3:
                return Vector3(0,0,0)
            case 4:
                return Vector3(0,0,0)
            case __:
                return Vector3(0,0,0)

    @staticmethod
    def test():
        """
        Test functionality of the StateMachine class.
        """
        print("Testing StateMachine...")

        class TestState(SignalEmitter):
            async def enter(self):
                print("Entering TestState")

            async def exit(self):
                print("Exiting TestState")

        state_machine = StateMachine()
        state_machine.state_list = [TestState]

        async def run_test():
            await state_machine.start()
            await asyncio.sleep(1)
            await state_machine.transition_to(0)

        asyncio.run(run_test())


if __name__ == "__main__": # This doesn't really work, but it opens the console, so we keep it around.
    StateMachine.test()
