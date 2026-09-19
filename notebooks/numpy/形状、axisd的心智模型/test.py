import numpy as np

a = np.array(
    [1,2,3,4,5]
    )
print(a.shape)
print(a.ndim)
print(a.dtype)

b = np.array(
    [
    [1,2,3,4],
    [7,4,5,6],
    [5,4,6,9]
    ]
)
print(b.shape)
#结果是（3,4）→（序列·数量，碱基类型·数量）
c = np.mean(b,axis= 0)
d = np.mean(b,axis= 1)
print(c,d)
print(c.shape,d.shape)
# c中的数字意味着：（平均）每个碱基类型的碱基数量，没有了序列的概念
# d中的数字意味着：（平均）每个序列有的碱基数量，没有了碱基类型的概念
e = np.array([1,2,3,4,5,6,7,8,9,10,11,12])
f = np.reshape(e,(3,4))
print(e)
print(f)

g=np.zeros([100,128])
print(g.shape,g.ndim)

