import numpy as np
def hamming_syndrome(block):
    block = np.asarray(block, dtype=np.int8)

    if block.shape != (7,):
        raise ValueError("Block must contain exactly 7 bits.")

    syndrome = 0

    for position, bit in enumerate(block, start=1):
        if bit:
            syndrome ^= position

    return syndrome


def hamming_reconcile(alice_key, bob_key):
    alice_key = np.asarray(alice_key, dtype=np.int8)
    bob_key = np.asarray(bob_key, dtype=np.int8)

    if alice_key.shape != bob_key.shape:
        raise ValueError("Keys must have equal lengths.")

    if not np.all(np.isin(alice_key, [0, 1])):
        raise ValueError("Alice's key must contain only bits.")

    if not np.all(np.isin(bob_key, [0, 1])):
        raise ValueError("Bob's key must contain only bits.")

    n_blocks = len(alice_key) // 7
    usable_length = 7 * n_blocks

    alice = alice_key[:usable_length].copy()
    bob = bob_key[:usable_length].copy()

    alice_blocks = alice.reshape(n_blocks, 7)
    bob_blocks = bob.reshape(n_blocks, 7)

    corrected = bob_blocks.copy()

    for i in range(n_blocks):
        s_alice = hamming_syndrome(alice_blocks[i])
        s_bob = hamming_syndrome(bob_blocks[i])

        error_syndrome = s_alice ^ s_bob

        if 1 <= error_syndrome <= 7:
            corrected[i, error_syndrome - 1] ^= 1

    return alice, corrected.ravel()
