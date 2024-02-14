from QuantumSimulator.QuantumDevice import Qubit, QuantumDevice

def prepare_classical_message(bit: bool, q: Qubit) -> None:
    if bit:
        q.x()

def eve_measure_plusminus(q: Qubit) -> bool:
    q.h()
    return q.measure()

def prepare_classical_message_plusminus(bit: bool, q: Qubit) -> None:
    if bit:
        q.x()
        
    q.h()

def send_classical_bit_plusminus(device: QuantumDevice, bit: bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message_plusminus(bit, q)
        result = eve_measure_plusminus(q)

        assert result == bit

def send_classical_bit_wrong_basis(device: QuantumDevice, bit: bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message(bit, q)
        result = eve_measure_plusminus(q)

        assert result == bit, "Bits have different values"