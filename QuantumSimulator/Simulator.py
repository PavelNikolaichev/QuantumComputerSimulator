import numpy as np
from QuantumSimulator.Qubit import Qubit
from QuantumSimulator.QuantumDevice import QuantumDevice

# Define constant qubits and Hardmand's operation

KET_0 = np.array([
    [1],
    [0]
], dtype=complex)

H = np.array([
    [1, 1],
    [1, -1]
], dtype=complex) / np.sqrt(2)

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex) / np.sqrt(2)

class SingleQubitSimulator(QuantumDevice):
    def __init__(self):
        pass

    def allocate_qubit(self) -> Qubit:
        return SimulatedQubit()
    
    def deallocate_qubit(self, qubit: Qubit):
        qubit.reset()

        del qubit


class SimulatedQubit(Qubit):
    def __init__(self):
        self.reset()

    def h(self):
        self.state = H @ self.state

    def x(self):
        self.state = X @ self.state

    def measure(self) -> bool:
        prob_0 = np.abs(self.state[0, 0]) ** 2
        measurements = np.random.random() <= prob_0 # Simulate quantum entanglement

        return False if measurements else True
    
    def reset(self):
        self.state = KET_0.copy()