import abc
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from QuantumSimulator.Qubit import Qubit

class QuantumDevice(metaclass=ABCMeta):
    @abstractmethod
    def allocate_qubit(self) -> Qubit:
        """
        Allocate a qubit from the device.
        """
        pass
    @abstractmethod
    def deallocate_qubit(self, qubit: Qubit):
        """
        Deallocate a qubit from the device.
        """
        pass
    @contextmanager
    def using_qubit(self):
        """
        Context manager to allocate a qubit from the device and deallocate it when the context is exited.
        """
        qubit = self.allocate_qubit()
        
        try:
            yield qubit
        finally:
            qubit.reset()

        self.deallocate_qubit(qubit)