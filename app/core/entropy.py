from collections import Counter
from math import log2
from pathlib import Path


DEFAULT_SAMPLE_SIZE = 65_536


def calculate_entropy(data: bytes) -> float:
    """Calculate Shannon entropy for a byte sequence.

    Returns a value between 0.0 and 8.0.
    """
    if not data:
        return 0.0

    counts = Counter(data)
    data_length = len(data)

    entropy = 0.0

    for count in counts.values():
        probability = count / data_length
        entropy -= probability * log2(probability)

    return entropy


def calculate_file_entropy(
    file_path: str | Path,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> float:
    """Calculate Shannon entropy from the beginning of a file.

    Only the first ``sample_size`` bytes are read to avoid loading
    large files completely into memory.
    """
    path = Path(file_path)

    if sample_size <= 0:
        raise ValueError("sample_size must be greater than zero")

    with path.open("rb") as file:
        sample = file.read(sample_size)

    return calculate_entropy(sample)
