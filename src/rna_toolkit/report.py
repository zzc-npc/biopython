from datetime import datetime
from pathlib import Path


def _md_table(headers, rows):
    """生成 Markdown 表格。"""
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def build_report(
    summary,
    base_counts,
    kmer_counter,
    k,
    top_n,
    input_path,
    command,
    out_file,
):
    """生成 report.md。"""
    total_base = sum(base_counts.values())

    stat_rows = [
        ["条数", summary["count"]],
        ["总长", summary["total_length"]],
        ["最短", summary["min_length"]],
        ["最长", summary["max_length"]],
        ["平均", f"{summary['mean_length']:.2f}"],
        ["中位数", summary["median_length"]],
        ["N50", summary["n50"]],
    ]

    base_rows = []
    for b in ["A", "C", "G", "U", "N", "other"]:
        c = base_counts.get(b, 0)
        pct = f"{c / total_base * 100:.2f}%" if total_base else "0%"
        base_rows.append([b, c, pct])

    kmer_rows = [[kmer, cnt] for kmer, cnt in kmer_counter.most_common(top_n)]

    lines = []
    lines.append("# RNA FASTA Report\n")
    lines.append("## 输入\n")
    lines.append(f"- 文件: `{input_path}`")
    lines.append(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("## 命令\n")
    lines.append("```bash")
    lines.append(command)
    lines.append("```\n")
    lines.append("## 基本统计\n")
    lines.append(_md_table(["指标", "值"], stat_rows))
    lines.append("\n## 碱基组成\n")
    lines.append(_md_table(["碱基", "数量", "比例"], base_rows))
    lines.append(f"\n## Top {top_n} k-mers (k={k})\n")
    lines.append(_md_table(["k-mer", "count"], kmer_rows))
    lines.append("\n## 图片\n")
    lines.append("![Length Distribution](figures/length_hist.png)\n")
    lines.append("![Base Composition](figures/base_composition.png)\n")
    lines.append("![Top k-mers](figures/kmer_top.png)\n")

    out_file.write_text("\n".join(lines), encoding="utf-8")
