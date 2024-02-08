from QuantumSimulator.QuantumDevice import QuantumDevice
from QuantumSimulator.Simulator import SingleQubitSimulator

def qnrg(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        return q.measure()
    
if __name__ == '__main__':
    qsim = SingleQubitSimulator()

    for sample_idx in range(10):
        sample = qnrg(qsim)

        print(f"Sample {sample_idx}: {sample}")