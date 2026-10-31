import numpy as np
import secrets
def binary_toeplitz_matrix(n, output_length, seed=None):

    if n <= 0 or output_length <= 0:
        raise ValueError("Lengths must be positive.")

    seed_length = n + output_length - 1

    if seed is None:
        random_bytes = secrets.token_bytes((seed_length + 7) // 8)
        seed = np.unpackbits(
            np.frombuffer(random_bytes, dtype=np.uint8)
        )[:seed_length]
    else:
        seed = np.asarray(seed, dtype=np.uint8).ravel()

        if len(seed) != seed_length:
            raise ValueError("Incorrect seed length.")

        if not np.all(np.isin(seed, [0, 1])):
            raise ValueError("Seed must contain binary values.")

    indices = (
        np.arange(output_length)[:, None]
        - np.arange(n)[None, :]
        + n - 1
    )

    T = seed[indices]

    return T, seed


def privacy_amplification(key, output_length, seed=None):

    key = np.asarray(key, dtype=np.uint8).ravel()

    if not np.all(np.isin(key, [0, 1])):
        raise ValueError("Key must contain only binary values.")

    if not 0 < output_length <= len(key):
        raise ValueError("Invalid output length.")

    T, seed = binary_toeplitz_matrix(
        len(key), output_length, seed
    )

    final_key = (T @ key) % 2

    return final_key.astype(np.uint8), seed



def binary_entropy(q):
    """Calculate binary entropy in bits."""

    if q < 0 or q > 1:
        raise ValueError("Probability must be between 0 and 1.")

    if q == 0 or q == 1:
        return 0.0

    return (
        -q * np.log2(q)
        -(1 - q) * np.log2(1 - q)
    )


def calculate_key_length(
    input_length,
    qber,
    leakage_ec,
    epsilon_pa=1e-10
):
    """
    Estimate the privacy-amplified key length.
    """

    if input_length <= 0:
        return 0

    if not 0 <= qber < 0.5:
        raise ValueError("Invalid QBER.")

    if leakage_ec < 0:
        raise ValueError("Leakage cannot be negative.")

    if not 0 < epsilon_pa < 1:
        raise ValueError("Invalid privacy parameter.")

    entropy = binary_entropy(qber)

    estimated_min_entropy = input_length * (1 - entropy)

    # Leftover hash lemma penalty.
    security_penalty = 2 * np.log2(1 / (2 * epsilon_pa))

    output_length = (
        estimated_min_entropy
        - leakage_ec
        - security_penalty
    )

    return max(0, min(input_length, int(np.floor(output_length))))
