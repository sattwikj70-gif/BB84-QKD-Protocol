from qiskit_aer.noise import NoiseModel, depolarizing_error,amplitude_damping_error,phase_damping_error,ReadoutError
def noise_creation(p_depol,p_amp,p_phase,p_readout):
    noise_model = NoiseModel()
    error_1q = depolarizing_error(p_depol, 1).compose(amplitude_damping_error(p_amp).compose(phase_damping_error(p_phase)))
    noise_model.add_all_qubit_quantum_error(error_1q, ['h', 'x'])
    readout_error = ReadoutError([[1 - p_readout, p_readout],[p_readout, 1 - p_readout],])
    noise_model.add_all_qubit_readout_error(readout_error)
    return noise_model