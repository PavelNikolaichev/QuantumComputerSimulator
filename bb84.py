from QuantumSimulator.QuantumDevice import QuantumDevice
from QuantumSimulator.Qubit import Qubit

from typing import List

from QuantumSimulator.Simulator import SingleQubitSimulator


def sample_random_bit(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        result = q.measure()
        q.reset()
    
    return result

def prepare_message_qubit(message: bool, basis: bool, q: Qubit) -> None:
    if message:
        q.x()
    
    if basis:
        q.h()

def measure_message_qubit(basis: bool, q: Qubit) -> bool:
    if basis:
        q.h()

    result = q.measure()
    q.reset()

    return result

def convert_to_hex(bits: List[bool]) -> str:
    return hex(int(''.join(["1" if bit else "0" for bit in bits]), 2))

def send_single_bit_bb84(device: QuantumDevice, target: QuantumDevice) -> tuple:
    [message, basis] = [sample_random_bit(device) for _ in range(2)]

    target_basis = sample_random_bit(target)

    with device.using_qubit() as q:
        prepare_message_qubit(message, basis, q)

        # Process of sending quantum message, our simulation doesn't requires this.

        target_message = measure_message_qubit(target_basis, q)

    return ((message, basis), (target_message, target_basis))

def simulate_bb84(n_bits: int) -> tuple:
    device = SingleQubitSimulator()
    target = SingleQubitSimulator()

    key = []
    iterations = 0

    while len(key) < n_bits:
        ((message, basis), (target_message, target_basis)) = send_single_bit_bb84(device, target)

        if basis == target_basis:
            key.append(message)
        
        iterations += 1
    
    print(f"Spent {iterations} to generate {n_bits}-bit key")

    return tuple(key)

def encrypt(message: List[bool], key: List[bool]) -> List[bool]:
    return [message_bit ^ key_bit for message_bit, key_bit in zip(message, key)]


if __name__ == '__main__':
    print("Simulating BB84 to generate a 96-bit key")

    key = simulate_bb84(96)
    print(f"Generated key: {convert_to_hex(key)}")

    message = [
        1, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        1, 0, 0, 1, 0, 1, 1, 0,
        1, 1, 0, 1, 1, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 1, 1, 0, 1,
        0, 0, 1, 1, 1, 1, 0, 1,
        1, 1, 0, 1, 1, 1, 0, 0,
        1, 0, 1, 1, 1, 0, 1, 1,
    ]

    print(f"Original message: {convert_to_hex(message)}")

    encrypted_message = encrypt(message, key)
    print(f"Encrypted message: {convert_to_hex(message)}")

    decrypted_message = encrypt(encrypted_message, key)
    print(f"Decrypted recieved message: {convert_to_hex(decrypted_message)}")