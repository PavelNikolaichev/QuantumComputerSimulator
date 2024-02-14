import random
from functools import partial
from typing import Tuple, Callable
import numpy as np
import qutip as qt

from QuantumSimulator import QuantumDevice, Qubit
from QuantumSimulator.Simulator import Simulator

Strategy = Tuple[Callable[[int], int], Callable[[int], int]]

def random_bit() -> int:
    return random.randint(0, 1)

def referee(strategy: Callable[[], Strategy]) -> bool:
    player, opponent = strategy()
    player_choice, opponent_choice = random_bit(), random_bit()
    
    parity = not(player(player_choice) == opponent(opponent_choice))

    return parity == (player_choice and opponent_choice)

def estimate_win_prob(strategy: Callable[[], Strategy], n: int = 1000) -> float:
    return sum(referee(strategy) for _ in range(n)) / n

def constant_strategy() -> Strategy:
    '''
    Always return 0.
    '''
    return (lambda _: 0, lambda _: 0)

def quantum_strategy(initial_state: qt.Qobj) -> Strategy:
    shared_system = Simulator(capacity=2)
    shared_system.register_state = initial_state
    
    player_qubit = shared_system.allocate_qubit()
    opponent_qubit = shared_system.allocate_qubit()

    shared_system.register_state = qt.bell_state()
    player_angles = [90 * np.pi / 180, 0]
    opponent_angles = [45 * np.pi / 180, 135 * np.pi / 180]

    def player(input: int) -> int:
        player_qubit.ry(player_angles[input])

        return player_qubit.measure()
    

    def opponent(input: int) -> int:
        opponent_qubit.ry(opponent_angles[input])

        return opponent_qubit.measure()

    return player, opponent

if __name__ == "__main__":
    constant_pr = estimate_win_prob(constant_strategy, 100)
    print(f"Constant strategy won {constant_pr:0.1%} of the time.")

    initial_state = qt.Qobj([[1], [0], [0], [1]]) / np.sqrt(2)
    quantum_pr = estimate_win_prob(partial(quantum_strategy, initial_state), 100)
    
    print(f"Quantum strategy won {quantum_pr:0.1%} of the time " \
          f"with initial state:\n{initial_state}.")