# rna-toolkit

RNA FASTA 工具箱：解析、统计、k-mer、可视化、报告。

## 功能

- FASTA / .fa.gz 解析，支持多行、空行、大小写、T/U 转换
- 长度统计：条数、总长、最短、最长、平均、中位数、N50
- 碱基组成：A / C / G / U / N / other，含 GC 含量
- k-mer 统计：k=1~5，输出 top N
- 可视化：长度分布、碱基比例、top k-mer
- 报告：summary.json、length_stats.csv、kmer_topN.csv、report.md

## 安装

    git clone <your-repo-url>
    cd biopython

    conda create -n rna_project python=3.12 -y
    conda activate rna_project

    pip install -e .
    pip install matplotlib pytest

## 使用

一条命令跑完统计、k-mer、图、报告：

    python -m rna_toolkit stats \
      --input data/test/test.fa \
      --out results/ \
      --kmer 2 \
      --top-n 10

只看帮助：

    python -m rna_toolkit --help
    python -m rna_toolkit stats --help

## 输出

    results/
    ├── summary.json          # 基本统计
    ├── length_stats.csv      # 每条序列的 header、length、gc_content
    ├── kmer_top10.csv        # top 10 k-mer
    ├── report.md             # Markdown 报告
    └── figures/
        ├── length_hist.png
        ├── base_composition.png
        └── kmer_top.png

## 项目结构

    biopython/
    ├── pyproject.toml
    ├── README.md
    ├── .gitignore
    ├── data/
    │   ├── raw/              # 原始数据，只读
    │   └── test/             # 小测试文件
    ├── results/              # 输出目录
    ├── src/
    │   └── rna_toolkit/
    │       ├── __init__.py
    │       ├── __main__.py   # python -m rna_toolkit 入口
    │       ├── cli.py        # argparse 主逻辑
    │       ├── fasta.py      # FASTA 解析
    │       ├── kmer.py       # k-mer 滑窗与计数
    │       ├── plots.py      # matplotlib 画图
    │       ├── report.py     # report.md 生成
    │       └── commands/     # CLI 子命令
    │           ├── __init__.py
    │           ├── stats.py
    │           └── kmer.py
    └── tests/
        ├── test_fasta.py
        ├── test_stats.py
        └── test_kmer.py

## 测试

    pytest -v

## 数据来源

- 测试数据：手写
- 真实数据：RNAcentral (https://rnacentral.org/)

## 依赖

- Python >= 3.10
- matplotlib
- pytest

## 许可

仅供学习与科研使用。
