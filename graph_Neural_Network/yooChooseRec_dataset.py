# 对图进行分类
import pickle
from pathlib import Path

import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import LabelEncoder
from torch_geometric.data import Data, InMemoryDataset
from tqdm import tqdm


class YooChooseBinaryDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return ['click_binary100m.pt']
        # return ['click_binary.pt']    # for whole dataset

    def download(self):
        pass

    def process(self):
        data_list = []
        # clicks = pd.read_csv(root / 'clicks_pro.csv', encoding='utf-8', low_memory=False)  # 使用全部数据
        clicks = pd.read_csv(root / 'clicks_pro_100m.csv', encoding='utf-8', low_memory=False)    # 使用部分数据

        # process by session_id
        grouped = iter(clicks.groupby('session_id'))
        lens = clicks.session_id.unique().shape[0]

        # clicks 不需要常驻内存, 并且使用动态加载
        del clicks

        for session_id, group in tqdm(grouped, total=lens):
            # 重新编码，作为节点的顺序
            sess_item_id = LabelEncoder().fit_transform(group.item_id)

            # 重建索引
            group = group.reset_index(drop=True)
            group['sess_item_id'] = sess_item_id

            # 节点的初始特征
            # 重复的浏览记录当做一次记录
            # 使用 item id 作为节点特征
            # 每个子表 group 都有同样的 session id
            node_features = group.loc[group.session_id == session_id, ['sess_item_id', 'item_id']].sort_values(
                'sess_item_id').item_id.drop_duplicates().values
            node_features = torch.LongTensor(node_features).unsqueeze(1)

            # 序列访问的顺序
            source_nodes = group.sess_item_id.values[:-1]
            target_nodes = group.sess_item_id.values[1:]
            edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)

            x = node_features    # item_id , 可以考虑使用 category
            y = torch.FloatTensor([group.label.values[0]])    # 对graph进行二分类，确定在该session下是否有购买行为

            # 每个 session 当做一个 graph
            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])


class YooChooseDatasetNode(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return []

    @property
    def processed_file_names(self):
        return ['buy_binary100m.pt']
        # return ['buy_binary.pt']    # for whole dataset

    def download(self):
        pass

    def process(self):
        data_list = []
        # clicks= pd.read_csv(root / 'clicks_pro.csv', encoding='utf-8', low_memory=False)  # 使用全部数据
        clicks = pd.read_csv(root / 'clicks_pro_100m.csv', encoding='utf-8', low_memory=False)    # 使用部分数据
        with open(root / 'buy_item_dict.pkl', 'rb') as f:
            buy_item_dict = pickle.load(f)

        # process by session_id
        grouped = iter(clicks.groupby('session_id'))
        lens = clicks.session_id.unique().shape[0]

        # buys 不需要常驻内存, 并且使用动态加载
        del clicks

        for session_id, group in tqdm(grouped, total=lens):
            # 重新编码，作为节点的顺序
            item_lb = LabelEncoder()
            sess_item_id = item_lb.fit_transform(group.item_id)

            # 重建索引
            group = group.reset_index(drop=True)
            group['sess_item_id'] = sess_item_id

            # 节点的初始特征
            # 重复的浏览记录当做一次记录
            # 使用 [item id, category] 作为节点特征
            node_features = group.loc[group.session_id ==
                                      session_id, ['sess_item_id', 'item_id', 'category']].sort_values('sess_item_id')[[
                                          'item_id', 'category'
                                      ]].drop_duplicates().values
            node_features = torch.LongTensor(node_features).unsqueeze(1)

            # 序列访问的顺序
            source_nodes = group.sess_item_id.values[:-1]
            target_nodes = group.sess_item_id.values[1:]
            edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)

            # 构造 x, y
            x = node_features

            if session_id in buy_item_dict:
                positive_indices = item_lb.transform(buy_item_dict[session_id])
                # one-hot 编码
                label = np.zeros(len(node_features))
                label[positive_indices] = 1
            else:
                label = [0] * len(node_features)

            y = torch.FloatTensor(label)

            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])


if __name__ == '__main__':
    #  测试
    root = Path('../data/yoochoose-data/')
    dataset = YooChooseBinaryDataset(root=root)

    with open(root / 'clicks_dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)

    dataset = YooChooseDatasetNode(root)

    with open(root / 'buys_dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)
