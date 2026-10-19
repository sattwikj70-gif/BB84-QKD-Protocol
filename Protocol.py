import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator
from Noise import noise_creation
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
noise_model=noise_creation(0.1)
simulator = AerSimulator(noise_model=noise_model)
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
#QBER calculation
index=rng.choice(np.sum(matching), size=500, replace=False)
vfa=alice_key[index]
vfb=bob_key[index]
new_alice_key=np.delete(alice_key,index)
new_bob_key=np.delete(bob_key,index)
sacrificed_bits= vfa==vfb
x=np.sum(sacrificed_bits)
qber=(500-x)/500
print('Qber=',qber*100)