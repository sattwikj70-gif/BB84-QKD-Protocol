import numpy as np
from scipy.sparse import csc_matrix
from ldpc.bplsd_decoder import BpLsdDecoder


def make_ldpc_matrix(n, rng, redundancy=0.30, column_weight=3):

    if n < 10:
        raise ValueError("Use a key block of at least 10 bits.")

    m = max(1, int(np.ceil(n * redundancy)))
    rows = []
    cols = []

    for j in range(n):
        selected_rows = rng.choice(
            m,
            size=min(column_weight, m),
            replace=False
        )
        rows.extend(selected_rows.tolist())
        cols.extend([j] * len(selected_rows))

    H = csc_matrix(
        (np.ones(len(rows), dtype=np.uint8), (rows, cols)),
        shape=(m, n),
        dtype=np.uint8
    )

    # Work over GF(2), so all entries are binary.
    H.data %= 2
    H.eliminate_zeros()

    return H


def ldpc_reconcile(alice_key, bob_key, qber,
                   redundancy=0.40, max_iter=50, seed=1234):
    """
    Syndrome-based LDPC reconciliation for a simulation.

    Returns:
        alice: Alice's retained key
        corrected_bob: Bob's corrected key, or None on failure
        success: whether decoding found a matching syndrome
        H: the parity-check matrix
        syndrome_leak: number of published syndrome bits
    """
    alice = np.asarray(alice_key, dtype=np.uint8).ravel()
    bob = np.asarray(bob_key, dtype=np.uint8).ravel()

    if len(alice) != len(bob):
        raise ValueError("Keys must have the same length.")

    if not np.all(np.isin(alice, [0, 1])):
        raise ValueError("Alice's key must contain only bits.")
    if not np.all(np.isin(bob, [0, 1])):
        raise ValueError("Bob's key must contain only bits.")
    if not 0 < qber < 0.5:
        raise ValueError("qber must be between 0 and 0.5.")

    rng = np.random.default_rng(seed)
    H = make_ldpc_matrix(len(alice), rng, redundancy)

    # Alice publishes her syndrome.
    s_alice = np.asarray(H @ alice).ravel() % 2

    # Bob calculates the syndrome of his own key.
    s_bob = np.asarray(H @ bob).ravel() % 2

    # The difference syndrome identifies the error pattern.
    syndrome = (s_alice ^ s_bob).astype(np.uint8)

    decoder = BpLsdDecoder(
        H,
        error_rate=float(qber),
        max_iter=max_iter,
        bp_method="product_sum",
        schedule="serial",
        lsd_method="lsd_cs",
        lsd_order=0
    )

    estimated_error = np.asarray(
        decoder.decode(syndrome),
        dtype=np.uint8
    ).ravel()

    if len(estimated_error) != len(bob):
        raise RuntimeError("Decoder returned an unexpected vector length.")

    corrected_bob = bob ^ estimated_error

    # Check whether the decoded error matches the syndrome.
    corrected_syndrome = (
        np.asarray(H @ corrected_bob).ravel() % 2
    )

    success = np.array_equal(corrected_syndrome, s_alice)

    if not success:
        corrected_bob = None

    return alice, corrected_bob, success, H, H.shape[0]
