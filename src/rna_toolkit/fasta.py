import gzip
from pathlib import Path
from typing import Iterator

def read_fasta(path: str) -> Iterator[tuple[str, str]]:
    """
    读取 FASTA 文件，逐条产出 (header, sequence)。
    支持 .fa 和 .fa.gz。
    """
    p = Path(path)

    if p.suffix == ".gz":
        f = gzip.open(p, "rt", encoding="utf-8")
    else:
        f = p.open("r", encoding="utf-8")

    with f:
        header = None
        seq_parts = []

        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    yield (header, "".join(seq_parts))
                header = line[1:].strip()
                seq_parts = []
            else:
                seq_parts.append(line.upper().replace("T", "U"))

        if header is not None:
            yield (header, "".join(seq_parts))