from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

class Qubit(metaclass=ABCMeta):
    @abstractmethod
    def swap(self, swap_target: "Qubit"):
        pass

    @abstractmethod
    def cnot(self, cnot_target: "Qubit"):
        pass

    @abstractmethod
    def h(self):
        """
        Transforms qubit using the Hardmard operation np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        """
        pass

    @abstractmethod
    def x(self):
        """
        Transforms qubit using the Hardmard operation np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        """
        pass

    @abstractmethod
    def y(self):
        pass

    @abstractmethod
    def z(self):
        pass

    @abstractmethod
    def ry(self, angle: float):
        """
        Calculate how far to rotate the qubit around the y-axis.
        """
        pass   

    @abstractmethod
    def measure(self) -> bool:
        """
        Measure qubit. In other words, extract data from it.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Method to simplify reset functionality
        """
        pass