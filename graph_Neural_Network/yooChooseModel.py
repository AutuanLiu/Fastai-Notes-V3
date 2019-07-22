import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import (SAGEConv, TopKPooling, global_max_pool, global_mean_pool)


class Net(nn.Module):
    def __init__(self, sparse_sz, emb_sz=128, p=0.5):
        super().__init__()

        self.item_embedding = torch.nn.Embedding(num_embeddings=sparse_sz, embedding_dim=emb_sz)
        self.conv1 = SAGEConv(emb_sz, 128)
        self.pool = TopKPooling(128, ratio=0.8)
        self.conv2 = SAGEConv(128, 128)
        self.fc1 = nn.Sequential(nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU())
        self.fc2 = nn.Sequential(nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU())
        self.drop = nn.Dropout(p)
        self.lin = nn.Linear(64, 1)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = self.item_embedding(x).squeeze(1)

        x = F.relu(self.conv1(x, edge_index))

        x, edge_index, _, batch, _ = self.pool(x, edge_index, None, batch)
        x1 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv2(x, edge_index))

        x, edge_index, _, batch, _ = self.pool(x, edge_index, None, batch)
        x2 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = F.relu(self.conv2(x, edge_index))

        x, edge_index, _, batch, _ = self.pool(x, edge_index, None, batch)
        x3 = torch.cat([global_max_pool(x, batch), global_mean_pool(x, batch)], dim=1)

        x = x1 + x2 + x3

        x = self.fc1(x)
        x = self.fc2(x)
        x = self.drop(x)
        x = torch.sigmoid(self.lin(x)).squeeze(1)
        return x
