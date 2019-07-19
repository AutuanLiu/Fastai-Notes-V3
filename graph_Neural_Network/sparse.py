# https://github.com/rusty1s/pytorch_sparse
import torch
from torch_sparse import coalesce, spmm, spspmm, transpose, eye

# 合并操作
# 这里是按照行优先的顺序
# 按行排序索引并删除重复项。重复的条目使用 torch_scatter 的聚合函数计算
# 即存在空行或者空列的情况，合并稀疏矩阵重复位置处的数值
# 合并后只有4个位置处有数值
index = torch.tensor([[1, 0, 1, 0, 2, 1], [0, 1, 1, 1, 0, 0]])
value = torch.Tensor([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]])

index, value = coalesce(index, value, m=3, n=2)
print(index, value, sep='\n')

# 聚合函数使用 平均值
index, value = coalesce(index, value, m=3, n=2, op='mean')
print(index, value, sep='\n')

# 转置，聚合函数默认为 add
index, value = transpose(index, value, 3, 2)
print(index, value, sep='\n')


# 稀疏矩阵 * 稠密矩阵
# index 表示稀疏矩阵的坐标，value表示对应的值
# 第一行是行坐标，第二行是列坐标
index = torch.tensor([[0, 0, 1, 2, 2], [0, 2, 1, 0, 1]])
value = torch.Tensor([1, 2, 4, 1, 3])
matrix = torch.Tensor([[1, 4], [2, 5], [3, 6]])

out = spmm(index, value, 3, matrix)
print(out)

# 稀疏矩阵 * 稀疏矩阵
indexA = torch.tensor([[0, 0, 1, 2, 2], [1, 2, 0, 0, 1]])
valueA = torch.Tensor([1, 2, 3, 4, 5])

indexB = torch.tensor([[0, 2], [1, 0]])
valueB = torch.Tensor([2, 4])

indexC, valueC = spspmm(indexA, valueA, indexB, valueB, 3, 3, 2)
print(indexC, valueC, sep='\n')

index, value = eye(4)
print(index, value, sep='\n')