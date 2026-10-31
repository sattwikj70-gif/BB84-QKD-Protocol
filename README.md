# BB84 Quantum Key Distribution Simulation

A Python-based simulation of the **BB84 Quantum Key Distribution (QKD) protocol**, incorporating intercept-resend eavesdropping, quantum channel noise, LDPC-based error reconciliation, and privacy amplification using universal hashing.
### Protocol Workflow

1. **Quantum State Preparation:** Alice generates random binary bits and encodes them using randomly selected Z and X measurement bases.
2. **Quantum Transmission:** The prepared qubits are transmitted through a simulated quantum channel.
3. **Eavesdropping Simulation:** Eve performs an intercept-resend attack with a configurable probability, measuring qubits in randomly selected bases.
4. **Measurement:** Bob independently chooses measurement bases and measures the received qubits.
5. **Key Sifting:** Alice and Bob retain only the bits for which their preparation and measurement bases match.
6. **Parameter Estimation:** A randomly selected subset of sifted bits is publicly compared to estimate the Quantum Bit Error Rate (QBER).
7. **Error Reconciliation:** LDPC syndrome-based decoding is used to correct discrepancies between Alice's and Bob's keys.
8. **Privacy Amplification:** Two-universal Toeplitz hashing compresses the reconciled key to reduce Eve's potential information.

## Features

- **BB84 Protocol:** Simulation of quantum state preparation, transmission and measurement using Qiskit.
- **Intercept-Resend Attack:** Configurable eavesdropping probability and random measurement bases.
- **Quantum Channel Noise:** Support for multiple noise mechanisms:
  - Depolarizing noise
  - Amplitude damping
  - Phase damping
  - Measurement readout errors
- **QBER Estimation:** Detection of channel disturbances through publicly sacrificed test bits.
- **LDPC Error Reconciliation:** Sparse parity-check matrices and syndrome-based decoding using Belief Propagation with Localised Statistics Decoding (BP+LSD).
- **Privacy Amplification:** Toeplitz matrix-based universal hashing over GF(2).
- **Secret Key Verification:** Comparison of Alice's and Bob's final keys.

## Project Structure

```text
BB84-QKD-Simulation/
│
├── Protocol.py
│   └── Main BB84 simulation and protocol workflow
│
├── Noise.py
│   └── Quantum channel noise model
│
├── ErrorCorrection.py
│   └── LDPC matrix generation and syndrome reconciliation
│
├── PrivacyAmplification.py
│   └── Toeplitz hashing and key-length estimation
│
└── README.md
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main implementation |
| NumPy | Binary operations and numerical computations |
| Qiskit | Quantum circuit construction |
| Qiskit Aer | Quantum circuit simulation |
| SciPy | Sparse matrix operations |
| LDPC | Belief Propagation and LSD decoding |

## Key Parameters

Several parameters can be modified to investigate the behaviour of the protocol.

| Parameter | Description |
|---|---|
| `N` | Number of transmitted quantum bits |
| `weights` | Probability distribution for Eve's interception |
| `p_depol` | Depolarizing noise probability |
| `p_amp` | Amplitude damping probability |
| `p_phase` | Phase damping probability |
| `p_readout` | Measurement readout error probability |
| `redundancy` | LDPC parity-check matrix redundancy |
| `max_iter` | Maximum decoding iterations |
| `epsilon_pa` | Privacy amplifion security parameter |


## Limitations
- The LDPC parity-check matrix uses a randomly generated sparse construction rather than an optimized code ensemble.
- The simulation uses a single-qubit circuit repeatedly rather than a physical optical communication channel.
- The QBER abort threshold is an illustrative asymptotic reference.
- The privacy amplification key-length calculation is an asymptotic educational estimate, not a rigorous finite-key security proof.
- A complete security analysis would require composable security bounds, finite-size statistical estimation, appropriate quantum min-entropy bounds, and a complete accounting of information leakage.
- Authentication of the classical communication channel is not implemented.

## Future Improvements

- Investigate optimized LDPC code constructions.
- Study the relationship between eavesdropping probability and QBER.
- Implement efficient Toeplitz hashing for larger key sizes.
- Compare simulated results with theoretical BB84 predictions.
