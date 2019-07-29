from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch import nn, optim
from torch_geometric.data import DataLoader

from yooChooseModel import Net
from yooChooseRec_dataset import YooChooseBinaryDataset


def train():
    model.train()

    loss_all = 0
    for data in train_loader:
        data = data.to(device)
        optimizer.zero_grad()
        output = model(data)

        label = data.y.to(device)
        loss = criterion(output, label)
        loss.backward()
        loss_all += data.num_graphs * loss.item()
        optimizer.step()
    return loss_all / len_train


@torch.no_grad()
def evaluate(loader):
    model.eval()

    predictions = []
    labels = []

    for data in loader:
        data = data.to(device)
        pred = model(data).detach().cpu().numpy()
        label = data.y.detach().cpu().numpy()
        predictions.append(pred)
        labels.append(label)

    predictions = np.hstack(predictions)
    labels = np.hstack(labels)
    return roc_auc_score(labels, predictions)


if __name__ == '__main__':
    #  各种设置
    lr, bs, ps = 0.001, 1024, 0.5
    sparse_sz, emb_sz = 37197, 128    # sparse_sz = clicks.item_id.max() + 1
    # sparse_sz, emb_sz = 48256, 128    # for whole dataset
    num_epochs = 10
    root = Path('../data/yoochoose-data/')
    device = torch.device('cuda: 0' if torch.cuda.is_available() else 'cpu')
    model = Net(sparse_sz, emb_sz=emb_sz, p=ps).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()

    # 数据集相关
    dataset = YooChooseBinaryDataset(root=root)
    dataset = dataset.shuffle()
    train_dataset, val_dataset, test_dataset = dataset[:800000], dataset[800000:900000], dataset[900000:]
    len_train = 800000

    # loaders
    train_loader = DataLoader(train_dataset, batch_size=bs)
    val_loader = DataLoader(val_dataset, batch_size=bs)
    test_loader = DataLoader(test_dataset, batch_size=bs)
    del dataset, train_dataset, val_dataset, test_dataset

    for epoch in range(num_epochs):
        loss = train()    # 训练

        # 评估
        train_auc = evaluate(train_loader)
        val_auc = evaluate(val_loader)
        test_auc = evaluate(test_loader)
        print(
            f'Epoch: {epoch:03d}, Loss: {loss:.5f}, Train Auc: {train_auc:.5f}, Val Auc: {val_auc:.5f}, Test Auc: {test_auc:.5f}'
        )

#  test auc: 0.78
