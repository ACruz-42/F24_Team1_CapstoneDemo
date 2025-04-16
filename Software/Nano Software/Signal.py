import asyncio
import logging


class Signal:
    """
    A signal that can be emitted and connected to.
    """

    def __init__(self, name):
        self.name = name
        self.connections = []
        self.logger = logging.getLogger("Nano")

    def connect(self, callable_obj):
        """
        Connect a callable to this signal. Returns signal.
        """
        if callable_obj not in self.connections:
            self.connections.append(callable_obj)
        return self

    def disconnect(self, callable_obj):
        """
        Disconnect a callable from this signal. Returns signal. TODO: Check why?
        """
        if callable_obj in self.connections:
            self.connections.remove(callable_obj)
        return self

    def disconnect_all(self) -> None:
        """
        Disconnects all callables from this signal
        """
        self.connections.clear()

    def emit(self, *args, **kwargs):
        """
        Emit the signal with the given arguments. Returns results immediately
        for synchronous functions.
        """
        # I made the below because I think it might be useful, but not necessary atm
        #self.logger.debug(f"Signal {self.name} called")
        results = []
        #self.logger.debug(f"Signal {self.name} emitted with {str(*args)} and {str(**kwargs)}")
        for callable_obj in self.connections:
            if not asyncio.iscoroutinefunction(callable_obj):
                # It's a normal function, call immediately
                results.append(callable_obj(*args, **kwargs))
            else:
                # For coroutines, we create a task but don't wait
                asyncio.create_task(callable_obj(*args, **kwargs))
        #self.logger.debug(f"Signal {self.name} emit returned with {str(results)}")
        return results

    async def emit_async(self, *args, **kwargs):
        """
        Async version that waits for all callbacks to complete, including coroutines.
        """
        results = []
        coroutines = []

        for callable_obj in self.connections:
            if asyncio.iscoroutinefunction(callable_obj):
                # It's an async function, add to coroutines list
                coroutines.append(callable_obj(*args, **kwargs))
            else:
                # It's a normal function, call immediately
                results.append(callable_obj(*args, **kwargs))

        # Wait for all coroutines to complete, if any
        if coroutines:
            coro_results = await asyncio.gather(*coroutines)
            results.extend(coro_results)

        return results

    def is_connected(self, callable_obj):
        """
        Check if a callable is connected to this signal. Returns it
        """
        return callable_obj in self.connections


class SignalEmitter:
    """
    A mixin-ish class that adds signal functionality to a class.
    """

    def __init__(self) -> None:
        self._signals = {}

    def add_signal(self, signal_name: str):
        """
            Makes a signal of name 'signal_name', adds it to internal signals, and then returns it
            Example usage:
            done = example_state.add_signal("done")
        """
        if signal_name not in self._signals:
            self._signals[signal_name] = Signal(signal_name)
        return self._signals[signal_name]

    def get_signal(self, signal_name):
        """
        Attempts to find signal of 'signal_name' if created and in internal signals. Returns it.
        """
        if signal_name not in self._signals:
            raise KeyError(f"Signal '{signal_name}' not found.")
        return self._signals[signal_name]

    def emit_signal(self, signal_name, *args, **kwargs):
        """
        Finds a signal of 'signal_name', if created and in internal signals. Emits it, and returns the results.
        """
        if signal_name not in self._signals:
            raise KeyError(f"Signal '{signal_name}' not found.")
        return self._signals[signal_name].emit(*args, **kwargs)

    def clear_signals(self) -> None:
        """
        Clears all signals
        :return:
        """
        for signal in self._signals:
            signal.disconnect_all()
