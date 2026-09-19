import csv
import json
from collections import Counter
from pathlib import Path

from rna_toolkit import read_fasta
from rna_toolkit.kmer import iter_kmers
from rna_toolkit.plots import plot_length_hist, plot_base_composition, plot_kmer_top
from rna_toolkit.report import build_report


def _n50(lengths):
    if not lengths:
        return 0
    total = sum(lengths)
    half = total / 2
    cum = 0
    for L in sorted(lengths, reverse=True):
        cum += L
        if cum >= half:
            return L
    return 0


def _median(lengths):
    if not lengths:
        return 0
    s = sorted(lengths)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def _gc_content(seq):
    if not seq:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)


def cmd_stats(args):
    path = Path(args.input)

    if not path.exists():
        print(f"错误: 文件不存在: {path}")
        raise SystemExit(1)

    lengths = []
    rows = []
    base_counts = Counter()
    kmer_counter = Counter()
    k = args.kmer
    top_n = args.top_n

    for header, seq in read_fasta(path):
        lengths.append(len(seq))
        rows.append({
            "header": header,
            "length": len(seq),
            "gc_content": round(_gc_content(seq), 4),
        })
        for ch in seq:
            if ch in "ACGU":
                base_counts[ch] += 1
            elif ch == "N":
                base_counts["N"] += 1
            else:
                base_counts["other"] += 1
        for kmer in iter_kmers(seq, k):
            kmer_counter[kmer] += 1

    if not lengths:
        print("错误: 文件里没有序列")
        raise SystemExit(1)

    summary = {
        "input": str(path),
        "count": len(lengths),
        "total_length": sum(lengths),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "mean_length": sum(lengths) / len(lengths),
        "median_length": _median(lengths),
        "n50": _n50(lengths),
    }

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # summary.json
    json_file = out_dir / "summary.json"
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # length_stats.csv
    csv_file = out_dir / "length_stats.csv"
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["header", "length", "gc_content"])
        writer.writeheader()
        writer.writerows(rows)

    # kmer_topN.csv
    kmer_file = out_dir / f"kmer_top{top_n}.csv"
    with kmer_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["kmer", "count"])
        for kmer, cnt in kmer_counter.most_common(top_n):
            writer.writerow([kmer, cnt])

    # 图
    plot_length_hist(lengths, figures_dir / "length_hist.png")
    plot_base_composition(base_counts, figures_dir / "base_composition.png")
    plot_kmer_top(kmer_counter, top_n, figures_dir / "kmer_top.png")

    # report.md
    report_file = out_dir / "report.md"
    command = (
        f"python -m rna_toolkit stats "
        f"--input {args.input} --out {args.out} "
        f"--kmer {k} --top-n {top_n}"
    )
    build_report(
        summary, base_counts, kmer_counter, k, top_n,
        input_path=args.input, command=command, out_file=report_file,
    )

    print(f"条数: {summary['count']}")
    print(f"总长: {summary['total_length']}")
    print(f"最短: {summary['min_length']}")
    print(f"最长: {summary['max_length']}")
    print(f"平均: {summary['mean_length']:.2f}")
    print(f"中位数: {summary['median_length']}")
    print(f"N50: {summary['n50']}")
    print(f"输出: {json_file}")
    print(f"输出: {csv_file}")
    print(f"输出: {kmer_file}")
    print(f"图: {figures_dir}")
    print(f"报告: {report_file}")


def register(subparsers):
    p = subparsers.add_parser("stats", help="统计 FASTA（含 k-mer、图、报告）")
    p.add_argument("--input", required=True, help="输入 FASTA 文件")
    p.add_argument("--out", required=True, help="输出目录")
    p.add_argument("--kmer", type=int, default=3, help="k-mer 长度")
    p.add_argument("--top-n", type=int, default=20, help="top N k-mer")
    p.set_defaults(func=cmd_stats)
