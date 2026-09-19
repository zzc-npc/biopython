from rna_toolkit.kmer import iter_kmers, count_kmers


def test_iter_kmers_basic():
    assert list(iter_kmers("ACGU", 2)) == ["AC", "CG", "GU"]


def test_iter_kmers_k_equals_l():
    assert list(iter_kmers("ACGU", 4)) == ["ACGU"]


def test_iter_kmers_k_larger_than_l():
    assert list(iter_kmers("AC", 3)) == []


def test_iter_kmers_k1():
    assert list(iter_kmers("ACGU", 1)) == ["A", "C", "G", "U"]


def test_count_kmers():
    c = count_kmers(["ACGU", "ACGUU"], 2)
    assert c["AC"] == 2
    assert c["CG"] == 2
    assert c["GU"] == 2
    assert c["UU"] == 1