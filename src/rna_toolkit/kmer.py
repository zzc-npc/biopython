from collections import Counter


def iter_kmers(seq, k):
    """逐个产出长度为 k 的子串。L < k 时不产出。"""
    L = len(seq)
    for i in range(max(0, L - k + 1)):
        yield seq[i:i + k]


def count_kmers(seqs, k):
    """统计所有序列的 k-mer 频数，返回 Counter。"""
    counter = Counter()
    for seq in seqs:
        for kmer in iter_kmers(seq, k):
            counter[kmer] += 1
    return counter
