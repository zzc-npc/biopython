from pathlib import Path

from rna_toolkit import read_fasta

DATA = Path(__file__).resolve().parent.parent / "data" / "test"


def test_read_fasta_simple():
    """测一个普通 FASTA，两条序列，含多行、空行、大小写、T/U。"""
    path = DATA / "test.fa"
    records = list(read_fasta(path))

    assert records == [("seq1", "ACGU"), ("seq2", "ACGUU")]


def test_read_fasta_gz():
    """测 .gz 和 .fa 结果一致。"""
    fa = DATA / "test.fa"
    gz = DATA / "test.fa.gz"

    assert list(read_fasta(fa)) == list(read_fasta(gz))


def test_empty_file(tmp_path):
    """空文件应返回空列表。"""
    f = tmp_path / "empty.fa"
    f.write_text("")

    assert list(read_fasta(f)) == []


def test_multiline_sequence(tmp_path):
    """多行序列应合并成一条，T 转 U，大写。"""
    f = tmp_path / "multi.fa"
    f.write_text(">a\nacg\nuu\n")

    assert list(read_fasta(f)) == [("a", "ACGUU")]


def test_blank_lines(tmp_path):
    """空行应跳过。"""
    f = tmp_path / "blank.fa"
    f.write_text(">a\n\nACGU\n\n>b\nUU\n")

    assert list(read_fasta(f)) == [("a", "ACGU"), ("b", "UU")]


def test_only_header(tmp_path):
    """只有 header 没有序列，应产出 ('a', '')。"""
    f = tmp_path / "only_header.fa"
    f.write_text(">a\n")

    assert list(read_fasta(f)) == [("a", "")]
