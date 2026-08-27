from app.core.entropy import calculate_entropy


def test_empty_data_has_zero_entropy():
    assert calculate_entropy(b"") == 0.0


def test_repeated_byte_has_zero_entropy():
    assert calculate_entropy(b"A" * 1000) == 0.0


def test_uniform_byte_distribution_has_maximum_entropy():
    data = bytes(range(256))
    assert calculate_entropy(data) == 8.0

def test_file_entropy_reads_file(tmp_path):
    test_file = tmp_path / "sample.bin"
    test_file.write_bytes(b"A" * 1000)

    from app.core.entropy import calculate_file_entropy

    assert calculate_file_entropy(test_file) == 0.0
