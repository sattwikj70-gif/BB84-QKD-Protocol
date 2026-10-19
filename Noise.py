from qiskit_aer.noise import NoiseModel, depolarizing_error
def noise_creation(p):
    noise_model = NoiseModel()
    error_1q = depolarizing_error(p, 1)
    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x', 'z'])
    return noise_model
