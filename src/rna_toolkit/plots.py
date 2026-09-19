from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 无界面后端，服务器也能跑
import matplotlib.pyplot as plt


def plot_length_hist(lengths, out_file):
    """长度分布直方图。"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(lengths, bins=50, color="steelblue", edgecolor="black")
    ax.set_title("Sequence Length Distribution")
    ax.set_xlabel("Length")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)


def plot_base_composition(base_counts, out_file):
    """碱基比例条形图。base_counts 是 dict 或 Counter。"""
    bases = ["A", "C", "G", "U", "N", "other"]
    counts = [base_counts.get(b, 0) for b in bases]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(bases, counts, color="seagreen", edgecolor="black")
    ax.set_title("Base Composition")
    ax.set_xlabel("Base")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)


def plot_kmer_top(counter, top_n, out_file):
    """top N k-mer 条形图。"""
    top = counter.most_common(top_n)
    if not top:
        return
    kmers = [k for k, _ in top]
    counts = [c for _, c in top]

    fig, ax = plt.subplots(figsize=(max(8, top_n * 0.5), 5))
    ax.bar(kmers, counts, color="coral", edgecolor="black")
    ax.set_title(f"Top {top_n} k-mers")
    ax.set_xlabel("k-mer")
    ax.set_ylabel("Count")
    plt.xticks(rotation=90)
    fig.tight_layout()
    fig.savefig(out_file, dpi=150)
    plt.close(fig)
