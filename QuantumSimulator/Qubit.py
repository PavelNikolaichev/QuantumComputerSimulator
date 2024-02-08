from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

class Qubit(metaclass=ABCMeta):
    @abstractmethod
    def h(self):
        """
        Transforms qubit using the Hardmard operation np.array([[1, 1], [1, -1]]) / np.sqrt(2)
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