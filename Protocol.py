import matplotlib.pyplot as plt
from random import randint
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator
c=ClassicalRegister(1)
q=QuantumRegister(1)
qc=QuantumCircuit(q,c)
Alice_Basis=[]
Bob_Basis=[]
bobs_bits=[]
Alices_bits=[]
Alice_key=[]
Bob_key=[]
simulator = AerSimulator()
for i in range(10):
    x = randint(0, 1)
    y = randint(0, 1)
    z = randint(0, 1)
    if x==1:
        qc.x(q[0])
        Alices_bits.append(1)
    else:
        Alices_bits.append(0)
    if y==1:
        qc.h(q[0])
        Alice_Basis.append('X')
    else:
        Alice_Basis.append('Z')

    qc.barrier(label="1")
    if z==1:
        qc.h(q[0])
        Bob_Basis.append('X')
    else:
        Bob_Basis.append('Z')
    qc.measure(q[0], c[0])
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1).result()
    counts = result.get_counts()
    bobs_bits.append(int(next(iter(counts))))
    qc.clear()
print(Alice_Basis,Bob_Basis)
print(Alices_bits,bobs_bits)
#Sifting process
for i in range(10):
    if Alice_Basis[i]==Bob_Basis[i]:
        Alice_key.append(Alices_bits[i])
        Bob_key.append(bobs_bits[i])
print(Alice_key,Bob_key)

