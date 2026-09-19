import argparse

from rna_toolkit.commands import stats, kmer


def build_parser():
    parser = argparse.ArgumentParser(
        prog="rna_toolkit",
        description="RNA FASTA toolkit",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="rna-toolkit 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    stats.register(subparsers)
    kmer.register(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
