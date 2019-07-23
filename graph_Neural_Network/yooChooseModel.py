# 使用 pyg1.3以上版本，SAGEConv在1.3.0版本存在bug
import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import (GraphConv, SAGEConv, TopKPooling, global_max_pool, global_mean_pool)
#  GraphConv, GateGraphConv, SGConv
# from sage_conv import SAGEConv


class Net(torch.nn.Module):
    def __init__(self, sparse_sz, emb_sz=128, p=0.5):
        super(Net, self).__init__()

        self.item_embedding = nn.Embedding(num_embeddings=sparse_sz, embedding_dim=emb_sz)

        self.conv1 = SAGEConv(emb_sz, 128)
        self.pool1 = TopKPooling(128, ratio=0.8)

        self.conv2 = SAGEConv(128, 128)
        self.pool2 = TopKPooling(128, ratio=0.8)

        self.conv3 = SAGEConv(128, 128)
        self.pool3 = TopKPooling(128, ratio=0.8)

        self.fc1 = nn.Sequential(nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU())
        self.fc2 = nn.Sequential(nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU())
        self.linear = nn.Linear(64, 1)
        self.drop = nn.Dropout(p)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = self.item_embedding(x).squeeze(1)

        x = F.relu(self.conv1(x, edge_index))
        x, edge_index, _, batch, *_ = self.pool1(x, edge_index, batch=batch)
        x1 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv2(x, edge_index))
        x, edge_index, _, batch, *_ = self.pool2(x, edge_index, batch=batch)
        x2 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv3(x, edge_index))
        x, edge_index, _, batch, *_ = self.pool3(x, edge_index, batch=batch)
        x3 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = x1 + x2 + x3

        x = self.fc1(x)
        x = self.fc2(x)
        x = self.drop(x)

        x = torch.sigmoid(self.linear(x)).squeeze(1)

        return x


class NetNode(nn.Module):
    def __init__(self, num_items, num_categories, emb_sz=128, p=0.5):
        super(Net, self).__init__()

        self.item_embedding = nn.Embedding(num_embeddings=num_items, embedding_dim=emb_sz)
        self.category_embedding = nn.Embedding(num_embeddings=num_categories, embedding_dim=emb_sz)
        self.conv1 = GraphConv(emb_sz * 2, 128)
        self.pool1 = TopKPooling(128, ratio=0.9)

        self.conv2 = GraphConv(128, 128)
        self.pool2 = TopKPooling(128, ratio=0.9)

        self.conv3 = GraphConv(128, 128)
        self.pool3 = TopKPooling(128, ratio=0.9)

        self.fc1 = nn.Sequential(nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU())
        self.fc2 = nn.Sequential(nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU())

        self.drop = nn.Dropout(p)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        item_id, category = x[:, :, 0], x[:, :, 1]

        emb_item = self.item_embedding(item_id).squeeze(1)
        emb_category = self.category_embedding(category).squeeze(1)

        x = torch.cat([emb_item, emb_category], dim=1)
        x = F.relu(self.conv1(x, edge_index))
        x, edge_index, _, batch, _ = self.pool1(x, edge_index, None, batch)
        x1 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv2(x, edge_index))
        x, edge_index, _, batch, _ = self.pool2(x, edge_index, None, batch)
        x2 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv3(x, edge_index))
        x, edge_index, _, batch, _ = self.pool3(x, edge_index, None, batch)
        x3 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = x1 + x2 + x3

        x = self.fc1(x)
        x = self.fc2(x)
        x = self.drop(x)
        x = F.relu(x)

        outputs = []
        for i in range(x.size(0)):
            output = torch.matmul(emb_item[data.batch == i], x[i, :])
            outputs.append(output)

        x = torch.cat(outputs, dim=0)
        x = torch.sigmoid(x)

        return x
