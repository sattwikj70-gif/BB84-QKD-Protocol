import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator
from Noise import noise_creation
from ErrorCorrection import hamming_reconcile
rng = np.random.default_rng()
N=100_000
alice_bits = rng.integers(0, 2, size=N)
alice_basis = rng.integers(0, 2, size=N)# 0 = Z basis, 1 = X basis
bob_basis = rng.integers(0, 2, size=N)
eve_basis=rng.integers(0, 2, size=N)
c=ClassicalRegister(N)
c1=ClassicalRegister(N)
q=QuantumRegister(1)
qc=QuantumCircuit(q,c,c1)
for i in range(N):
    qc.reset(q[0])
    if alice_bits[i]:
        qc.x(q[0])
    if alice_basis[i]:
        qc.h(q[0])
    #Eve attack
    '''if eve_basis[i]:
        qc.h(q[0])
    qc.measure(q[0],c1[i])
    if eve_basis[i]:
        qc.h(q[0])'''
    if bob_basis[i]:
        qc.h(q[0])
    qc.measure(q[0], c[i])
noise_model=noise_creation(0.01,0.01,0.01,0.01)
simulator = AerSimulator(noise_model=noise_model)
compiled = transpile(qc, simulator, optimization_level=0)
result = simulator.run(compiled, shots=1, memory=True).result()
measured = result.get_memory()[0]
eve_str, bob_str = measured.split()
bob_bits = np.fromiter(
    (int(bit) for bit in bob_str[::-1]),
    dtype=np.int8,
    count=N
)
matching = alice_basis == bob_basis
alice_key = alice_bits[matching]
bob_key = bob_bits[matching]
print("Transmitted bits:", N)
print("Matching bases:", np.sum(matching))
#QBER calculation
index=rng.choice(np.sum(matching), size=5000, replace=False)
vfa=alice_key[index]
vfb=bob_key[index]
sacrificed_bits= vfa==vfb
x=np.sum(sacrificed_bits)
qber=(5000-x)/5000
print('Qber=',qber*100)
alice_key_after_sifting=np.delete(alice_key,index)
bob_key_after_sifting=np.delete(bob_key,index)
alice_ec = alice_key_after_sifting.copy()
bob_before_ec = bob_key_after_sifting.copy()

alice_ec, bob_ec = hamming_reconcile(
    alice_ec, bob_before_ec
)

errors_before = np.count_nonzero(
    alice_ec != bob_before_ec[:len(alice_ec)]
)

errors_after = np.count_nonzero(alice_ec != bob_ec)

print("Errors before correction:", errors_before)
print("Errors after correction:", errors_after)

if len(alice_ec):
    print("Residual QBER (%):",
          100 * errors_after / len(alice_ec))
else:
    print("No complete blocks available.")
