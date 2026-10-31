import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator
from Noise import noise_creation
from ErrorCorrection import ldpc_reconcile
def eve_attack():
    if eve_basis[i]:
        qc.h(q[0])
    qc.measure(q[0],c1[i])
    if eve_basis[i]:
        qc.h(q[0])
weights=[0.8,0.2]
rng = np.random.default_rng()
N=100_000
alice_bits = rng.integers(0, 2, size=N)
alice_basis = rng.integers(0, 2, size=N)# 0 = Z basis, 1 = X basis
bob_basis = rng.integers(0, 2, size=N)
eve_basis=rng.integers(0, 2, size=N)
eve_chance=rng.choice([0,1], size=N, p=weights)
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
    if eve_chance[i]:
        eve_attack()
    if bob_basis[i]:
        qc.h(q[0])
    qc.measure(q[0], c[i])
noise_model=noise_creation(0,0,0,0)
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
# Illustrative asymptotic BB84 abort threshold.
# A real implementation needs a finite-key security analysis.
if qber >= 0.11:
    print("Abort: QBER is too high for this BB84 configuration.")
else:
    # The decoder requires a positive error-rate estimate.
    decoder_qber = max(qber, 1e-4)

    alice_ec, bob_ec, success, H, leakage = ldpc_reconcile(
        alice_key_after_sifting,
        bob_key_after_sifting,
        qber=decoder_qber,
        redundancy=0.40,
        max_iter=50
    )

    print("LDPC parity checks:", H.shape[0])
    print("Published syndrome bits:", leakage)

    if success:
        from PrivacyAmplification import (
            privacy_amplification,
            calculate_key_length
        )

        # Check actual reconciliation, not just syndrome agreement.
        if not np.array_equal(alice_ec, bob_ec):
            print("Reconciliation verification failed.")
        else:
            print("Reconciliation verified.")

            # Calculate the privacy-amplified key length.
            key_length = calculate_key_length(
                input_length=len(alice_ec),
                qber=qber,
                leakage_ec=leakage,
                epsilon_pa=1e-10
            )

            if key_length == 0:
                print("Insufficient entropy for a secret key.")

            else:
                # Alice chooses the public Toeplitz seed.
                alice_final, seed = privacy_amplification(
                    alice_ec,
                    key_length
                )

                # Bob uses exactly the same public seed.
                bob_final, _ = privacy_amplification(
                    bob_ec,
                    key_length,
                    seed=seed
                )

                print("Reconciled key length:", len(alice_ec))
                print("Final key length:", key_length)

                print(
                    "Alice and Bob final keys match:",
                    np.array_equal(alice_final, bob_final)
                )

                print("Final secret key:", alice_final)
