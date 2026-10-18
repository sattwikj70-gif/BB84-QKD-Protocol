from gc import get_count

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator

rng = np.random.default_rng()
N=100_000
alice_bits = rng.integers(0, 2, size=N)
alice_basis = rng.integers(0, 2, size=N)# 0 = Z basis, 1 = X basis
bob_basis = rng.integers(0, 2, size=N)
c=ClassicalRegister(N)
q=QuantumRegister(1)
qc=QuantumCircuit(q,c)
for i in range(N):
    qc.reset(q[0])
    if alice_bits[i]:
        qc.x(q[0])
    if alice_basis[i]:
        qc.h(q[0])
    if bob_basis[i]:
        qc.h(q[0])
    qc.measure(q[0], c[i])
simulator = AerSimulator()
compiled = transpile(qc, simulator, optimization_level=0)
result = simulator.run(compiled, shots=1, memory=True).result()
measured = result.get_memory()[0][::-1]
bob_bits = np.fromiter(
    (int(bit) for bit in measured), dtype=np.int8, count=N
)
matching = alice_basis == bob_basis
alice_key = alice_bits[matching]
bob_key = bob_bits[matching]
print("Transmitted bits:", N)
print("Matching bases:", np.sum(matching))
print("Alice's sifted key:", alice_key)
print("Bob's sifted key:", bob_key)
print("Keys identical:", np.array_equal(alice_key, bob_key))