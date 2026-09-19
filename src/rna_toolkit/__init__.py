from .fasta import read_fasta
#从同一个包fasta.py中导入函数，.表示当前包
__all__ = ["read_fasta"]
#from rna_toolkit import时暴露什么，就是其他人能用什么