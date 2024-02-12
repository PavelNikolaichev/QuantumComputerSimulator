from QuantumSimulator.QuantumDevice import QuantumDevice
from QuantumSimulator.Qubit import Qubit
from QuantumSimulator.Simulator import SingleQubitSimulator

def prepare_classical_message(bit: bool, q: Qubit) -> None:
    if bit:
        q.x()

def eve_measure(q: Qubit) -> bool:
    # Eve measures the qubit. Consider this a very very primitive exchange(since we share the same device)
    return q.measure()

def send_classical_bit(device: QuantumDevice, bit: bool) -> None:
    with device.using_qubit() as q:
        prepare_classical_message(bit, q)
        result = eve_measure(q)
        q.reset()

    assert result == bit

def qnrg(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        return q.measure()
    
if __name__ == '__main__':
    qsim = SingleQubitSimulator()
    message = qnrg(qsim)

    with qsim.using_qubit() as q:
        print("Sending message: ", message)
        prepare_classical_message(message, q)
        print("Eve measures: ", eve_measure(q))
