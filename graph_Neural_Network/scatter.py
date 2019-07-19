# https://pytorch-scatter.readthedocs.io/en/latest/functions/add.html
import torch
from torch_scatter import (scatter_add, scatter_div, scatter_max, scatter_mean, scatter_min, scatter_mul, scatter_std, scatter_sub)

# 二维
src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])
out = src.new_zeros((2, 6))

out = scatter_add(src, index, out=out)
print(out)
# tensor([[0., 0., 4., 3., 3., 0.], [2., 4., 4., 0., 0., 0.]])

# 不指定 out 给出 dim_size
src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])

out = scatter_add(src, index, dim_size=8)
print(out)
# tensor([[0., 0., 4., 3., 3., 0., 0., 0.], [2., 4., 4., 0., 0., 0., 0., 0.]])

# 不指定 out 并且不给出 dim_size（使用最小的dim_size）
src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
index = torch.tensor([[4, 1, 4, 2, 3], [0, 0, 2, 2, 1]])

out = scatter_add(src, index)
print(out)
# tensor([[0., 0., 4., 3., 3.], [2., 4., 4., 0., 0.]])

# 不指定 out 并且不给出 dim_size（使用最小的dim_size）
src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])

out = scatter_add(src, index, dim=0, dim_size=8)
print(out)
# tensor([[0., 2., 0., 0., 0.],
# [0., 0., 0., 0., 4.],
# [0., 0., 1., 7., 0.],
# [0., 0., 0., 0., 3.],
# [2., 0., 1., 0., 0.],
# [0., 0., 0., 0., 0.],
# [0., 0., 0., 0., 0.],
# [0., 0., 0., 0., 0.]])

# 一维
src = torch.Tensor([2, 0, 1, 4, 3])
index = torch.tensor([4, 1, 4, 2, 3])

out = scatter_add(src, index)
print(out)
# tensor([0., 0., 4., 3., 3.])

# 除法
src = torch.Tensor([[2, 1, 1, 4, 2], [1, 2, 1, 2, 4]]).float()
index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])
out = src.new_ones((2, 6))

out = scatter_div(src, index, out=out)

print(out)
# tensor([[1.0000, 1.0000, 0.2500, 0.5000, 0.5000, 1.0000],
# [0.5000, 0.2500, 0.5000, 1.0000, 1.0000, 1.0000]])

# 最大最小平均值
src = torch.Tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])
out, argmax = scatter_max(src, index)
print(out, argmax)

out, argmin = scatter_min(src, index)
print(out, argmin)

out = scatter_mean(src, index)
print(out)

out = scatter_mul(src, index)
print(out)

out = scatter_std(src, index)
print(out)

out = scatter_sub(src, index)
print(out)
