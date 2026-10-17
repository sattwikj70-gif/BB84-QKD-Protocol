import matplotlib.pyplot as plt
from random import randint
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister,transpile
from qiskit_aer import AerSimulator
c=ClassicalRegister(1)
q=QuantumRegister(1)
qc=QuantumCircuit(q,c)
Alice_Basis=[]
Bob_Basis=[]
for i in range(10):
    x = randint(0, 1)
    y = randint(0, 1)
    z = randint(0, 1)
    if x==1:
        qc.h(q[0])
        Alice_Basis.append('X')
    else:
        Alice_Basis.append('Z')
    if y==1:
        qc.x(q[0])
    qc.barrier(label="1")
    if z==1:
        qc.h(q[0])
        Bob_Basis.append('X')
    else:
        Bob_Basis.append('Z')
    qc.measure(q[0], c[0])
    qc.draw('mpl')
    qc.clear()
plt.text( 0.05, -1.6, "1:Alice's Process")
plt.show()
simulator=AerSimulator()
compiled=transpile(qc,simulator)
result=simulator.run(compiled,shots=10).result()
counts=result.get_counts()
bob_bit = int(next(iter(counts)))
print(Alice_Basis,Bob_Basis)
'''
print("Bob's measured bit:", bob_bit)
print("Bases match:", x == z)

if x==z:
    print("Ideal channel: Bob should recover Alice's bit.")
else:
    print("Bases differ: Bob's result is random.")'''