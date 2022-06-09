# %%
import torch
from torch.utils.data import Dataset

import numpy as np
import pandas as pd


# %%
class TagWhiskeyInterDataset(Dataset):
    def __init__(self, sep=',', threshold=86):
        root = '/opt/ml/workspace/team_git/Dataset/'
        df_iid = pd.read_csv(root+'whiskey_id.csv', sep=sep)
        # self.df_inter = pd.read_csv(root+'tag_whiskey_interaction.csv', sep=sep)
        self.df_inter = pd.read_csv(root+'tag_whiskey_interaction_norm.csv', sep=sep)
        
        self.encoder = df_iid.set_index('whiskey').to_dict()['iid']
        self.decoder = df_iid.set_index('iid').to_dict()['whiskey']
        self.df_inter['whiskey'] = self.df_inter['whiskey'].map(lambda x: self.encoder[x])
        self.df_inter['rating'] = self.df_inter['rating'].map(lambda x: self.__threshold_rating(x, threshold))
        
        self.df_inter = self.df_inter.reindex(columns=['rating', 'whiskey', 'body', 'sweet', 'sherry', 'malt', 'aperitif',
       'smoky', 'pungent', 'fruity', 'honey', 'floral', 'spicy', 'medicinal', 'nutty', 'winey'])
        
        array_inter = self.df_inter.to_numpy()
        
        self.items = torch.Tensor(array_inter[:, 1:])
        self.targets = torch.Tensor(array_inter[:, 0])
        self.field_dims = [len(df_iid)]
        
    def __len__(self):
        return self.targets.shape[0]

    def __getitem__(self, index):
        return self.items[index], self.targets[index]
    
    def __threshold_rating(self, rating, threshold):
        return 1 if rating >= threshold else 0

# %%
if __name__=='__main__':
    from IPython.display import display
    
    dataset = TagWhiskeyInterDataset()
    display(dataset.df_inter)
    print(dataset.encoder)
    print(dataset.decoder)
    print(dataset[0])
    print(len(dataset))
# %%
