import csv
from pathlib import Path

from rna_toolkit import read_fasta
from rna_toolkit.kmer import count_kmers
from rna_toolkit.plots import plot_kmer_top


def cmd_kmer(args):
    path = Path(args.input)

    if not path.exists():
        print(f"错误: 文件不存在: {path}")
        raise SystemExit(1)

    seqs = (seq for header, seq in read_fasta(path))
    counter = count_kmers(seqs, args.kmer)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"kmer_top{args.top_n}.csv"

    with out_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["kmer", "count"])
        for kmer, count in counter.most_common(args.top_n):
            writer.writerow([kmer, count])

    # 画图
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    plot_kmer_top(counter, args.top_n, figures_dir / "kmer_top.png")

    print(f"k = {args.kmer}")
    print(f"不同 k-mer 数: {len(counter)}")
    print(f"输出: {out_file}")
    print(f"图: {figures_dir / 'kmer_top.png'}")


def register(subparsers):
    p = subparsers.add_parser("kmer", help="统计 k-mer")
    p.add_argument("--input", required=True, help="输入 FASTA 文件")
    p.add_argument("--out", required=True, help="输出目录")
    p.add_argument("--kmer", type=int, default=3, help="k-mer 长度")
    p.add_argument("--top-n", type=int, default=20, help="top N k-mer")
    p.set_defaults(func=cmd_kmer)
