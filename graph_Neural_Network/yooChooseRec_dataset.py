import gc
import torch
import pickle
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from torch_geometric.data import InMemoryDataset, Data
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
        return [Path(self.processed_dir)/'click_binary.pt']

    def download(self):
        pass

    def process(self):
        data_list = []
        clicks = pd.read_csv(root/'clicks_pro.csv', encoding='utf-8', low_memory=False)
        # process by session_id
        grouped = clicks.groupby('session_id')

        for session_id, group in tqdm(grouped):
            # 重新编码，作为节点的顺序
            # sess_item_id = LabelEncoder().fit_transform(group.item_id)

            # 重建索引
            # group = group.reset_index(drop=True)
            group['sess_item_id'] = LabelEncoder().fit_transform(group.item_id)
            
            # 节点的初始特征
            # 重复的浏览记录当做一次记录
            # 使用 item id 作为节点特征
            # 每个子表 group 都有同样的 session id
            node_features = group.loc[group.session_id == session_id, ['sess_item_id', 'item_id']].sort_values('sess_item_id').item_id.drop_duplicates().values
            node_features = torch.LongTensor(node_features).unsqueeze(1)

            # 序列访问的顺序
            source_nodes = group.sess_item_id.values[:-1]
            target_nodes = group.sess_item_id.values[1:]
            edge_index = torch.tensor([source_nodes, target_nodes], dtype=torch.long)

            x = node_features
            y = torch.FloatTensor([group.label.values[0]])

            # 每个 session 当做一个 graph
            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])


if __name__ ==   '__main__':
    root = Path('../data/yoochoose-data/')
    dataset  =  YooChooseBinaryDataset(root=root)

    with open(root/'clicks_dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)
