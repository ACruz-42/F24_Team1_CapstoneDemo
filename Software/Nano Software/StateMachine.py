from typing import List
from RoverStates import *
import asyncio
from datetime import datetime
class StateMachine(SignalEmitter):
    def __init__(self):
        SignalEmitter.__init__(self)
        self.logger = None
        self.transform_requested = self.add_signal("transform_requested")
        self.request_light_detected = self.add_signal("request_light_detected")
        self.current_state: State = None
        self.current_index: int = 0
        self.time = datetime.now()
        # self.state_list: List = [WaitState, SenseState, BeaconState, GCSCState, NCSCState, CavePrepState,
        #                              CaveVacuumState, MaterialPickupState]
        self.state_list: List = [ShowcaseState]

        self.nsc_loaded = False
        self.gsc_loaded = False
        self.expanded = False
        self.loading_zone = -1

        self.testing = False  # For testing purposes, do not set to True

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
            await self.current_state.exit()

        self.current_index = index
        self.current_state = self.state_list[index]()
        async def transition_to_next(): await self.transition_to(self.current_index + 1)
        self.current_state.done.connect(transition_to_next)
        self.current_state.transform_request.connect(self.transform_requested.emit)

        await self.current_state.enter()

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
