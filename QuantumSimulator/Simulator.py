import numpy as np 
import qutip as qt
from qutip.qip.operations import hadamard_transform, gate_expand_1toN, gate_expand_2toN
from typing import List

from QuantumSimulator.Qubit import Qubit
from QuantumSimulator.QuantumDevice import QuantumDevice

# Define constant qubits and Hardmand's operation

KET_0 = qt.basis(2, 0)
H = hadamard_transform()


class SimulatedQubit(Qubit):
    def __init__(self, parent: "Simulator", id: int):
        self.parent = parent
        self.id = id

    def h(self) -> None:
        self.parent._apply(H, [self.id])

    def measure(self) -> bool:
        projectors = [
            gate_expand_1toN(
                qt.basis(2, outcome) * qt.basis(2, outcome).dag(),
                self.parent.capacity,
                self.id
            )
            for outcome in (0, 1)
        ]

        post_measurement_states = [
            projector * self.parent.register_state
            for projector in projectors
        ]

        probabilities = [
            post_measurement_state.norm() ** 2
            for post_measurement_state in post_measurement_states
        ]

        sample = np.random.choice([0, 1], p=probabilities)
        self.parent.register_state = post_measurement_states[sample].unit()

        return bool(sample)

    def swap(self, target: Qubit) -> None:
        self.parent._apply(
            qt.swap(),
            [self.id, target.id]
        )

    def cnot(self, target: Qubit) -> None:
        self.parent._apply(
            qt.cnot(),
            [self.id, target.id]
        )

    def rx(self, theta: float) -> None:
        self.parent._apply(qt.rx(theta), [self.id])

    def ry(self, theta: float) -> None:
        self.parent._apply(qt.ry(theta), [self.id])

    def rz(self, theta: float) -> None:
        self.parent._apply(qt.rz(theta), [self.id])

    def x(self) -> None:
        self.parent._apply(qt.sigmax(), [self.id])

    def y(self) -> None:
        self.parent._apply(qt.sigmay(), [self.id])

    def z(self) -> None:
        self.parent._apply(qt.sigmaz(), [self.id])
    
    def reset(self):
        if self.measure():
            self.x()


class Simulator(QuantumDevice):
    def __init__(self, capacity: int = 3):
        self.capacity = capacity

        self.available_qubits = [SimulatedQubit(self, _) for _ in range(capacity)]
        self._sort_available()

        self.register_state = qt.tensor(*[qt.basis(2, 0) for _ in range(capacity)])

    def _sort_available(self) -> None:
        self.available_qubits = list(sorted(self.available_qubits, key=lambda qubit: qubit.id, reverse=True))


    def allocate_qubit(self) -> SimulatedQubit|None:
        if len(self.available_qubits) > 0:
            return self.available_qubits.pop()
    
    def deallocate_qubit(self, qubit: SimulatedQubit):
        self.available_qubits.append(qubit)
        self._sort_available()

    def _apply(self, unitary: qt.Qobj, ids: List[int]):
        if len(ids) == 1:
            matrix = gate_expand_1toN(unitary, self.capacity, ids[0])
        elif len(ids) == 2:
            matrix = gate_expand_2toN(unitary, self.capacity, *ids)
        else:
            raise ValueError("Only one- or two-qubit unitary matrices supported.")
        
        self.register_state = matrix * self.register_state
        
    def dump(self) -> None:
        print(self.register_state)