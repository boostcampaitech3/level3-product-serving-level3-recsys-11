# %%
from recbole.quick_start.quick_start import load_data_and_model
from recbole.data.dataloader.user_dataloader import UserDataLoader

import pandas as pd
import numpy as np
import torch

from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import MinMaxScaler

from typing import Dict
from pathlib import Path
from collections import defaultdict


DICT_RANGE_COST = {
    "$":        (0,     30),
    "$$":       (30,    50),
    "$$$":      (50,    70),
    "$$$$":     (70,    125),
    "$$$$$":    (125,   300),
    "$$$$$+":   (300,   np.inf),
}
LIST_COST = list(DICT_RANGE_COST.keys())
LEN_LIST_COST = len(LIST_COST)

# 모델 불러오기 기능
def  initiate(CONFIG):
    config, model, dataset, dataloader, _, _ = load_data_and_model(
            model_file= Path((CONFIG['dir_model_saved'])) / CONFIG['file_model_used'],
        )
    return config, model, dataset, dataloader, _, _

def filter_by_price(CONFIG, df_cluster, _price_min, _price_max):               
    list_cost_allowed = filter_Cost_by_price(CONFIG, _price_min, _price_max)
    
    condition = df_cluster.Cost.isin(list_cost_allowed)
    return df_cluster[condition]

def filter_Cost_by_price(CONFIG, _price_min, _price_max):
    if _price_min > _price_max:
        tmp = _price_min
        _price_min = _price_max
        _price_max = tmp
    
    idx_min = find_idx_range_cost(CONFIG, _price_min)
    idx_max = find_idx_range_cost(CONFIG, _price_max)
    
    if idx_min==idx_max:
        return LIST_COST[idx_min:idx_max+1]
    
    idx_max = None if idx_max+1==LEN_LIST_COST else idx_max
    return LIST_COST[idx_min:idx_max]

def find_idx_range_cost(CONFIG, val, min=True):
    won_per_cad = CONFIG['won_per_cad']
    val = val / won_per_cad
    
    for idx, (k, (v_min, v_max)) in enumerate(DICT_RANGE_COST.items()):
        if (v_min <= val < v_max) & min:
            return idx
        elif (v_min < val <= v_max) & (not min):
            return idx
    raise IndexError


class pop_rec():
    def __init__(self,CONFIG) -> None:
        self.CONFIG=CONFIG
    
    def _popularity(self, k:int=10, _price_min:int=0, _price_max:int=1000000) -> list:
        list_pop = []
        dir_Pop = Path(self.CONFIG['dir_dataset']) / self.CONFIG['name_dataset'] / f'Pop.csv'
        iterator = pd.read_csv(dir_Pop).iterrows()
        
        df_feature = pd.read_csv(self.CONFIG['dir_source_of_item'], sep=self.CONFIG['sep_source'], index_col='Whiskey')
        list_cost_allowed = filter_Cost_by_price(self.CONFIG, _price_min, _price_max)
        
        for idx, row in iterator:
            whiskey = row['whiskey']
            
            whiskey = whiskey.replace('ä', 'a')
            whiskey = whiskey.replace('é', 'e')
            if whiskey=='[PAD]':continue
            
            if len(list_pop) == k:
                break
            if not df_feature.loc[whiskey].Cost in list_cost_allowed:
                continue
            list_pop.append(whiskey)
        return list_pop

    
class tag_rec():
    def __init__(self,CONFIG) -> None:
        self.CONFIG=CONFIG
        self.df_whisky = pd.read_csv(self.CONFIG['dir_integration'], sep=self.CONFIG['sep_source'])
        self.cluster2taste = pd.read_csv(self.CONFIG['dir_whiskey_cluster'], sep=self.CONFIG['sep_source']).set_index('Cluster')
        self.minmaxscaler = MinMaxScaler()
        self.dict_range_cost = {
            "$":        (0,     30),
            "$$":       (30,    50),
            "$$$":      (50,    70),
            "$$$$":     (70,    125),
            "$$$$$":    (125,   300),
            "$$$$$+":   (300,   np.inf),
        }
        self.list_cost = list(self.dict_range_cost.keys())
    
    def _cal_cos_sim(self, dict_taste:Dict[str, str], organized=False) -> np.ndarray:
        _dict_taste = defaultdict(float)
        _dict_taste.update(dict_taste)
        col_taste = self.cluster2taste.columns
        
        list_taste = [_dict_taste[k] for k in col_taste]
        list_taste = [list_taste]
        
        sim = cosine_distances(self.cluster2taste, list_taste)
        
        if organized:
            self.minmaxscaler.fit(sim)
            sim = self.minmaxscaler.transform(sim)
    
        return sim
    
    def find_cluster(self, dict_taste:Dict[str, str]) -> str:
        array_cluster = self._cal_cos_sim(dict_taste)
        idx_cluster = array_cluster.argmin()
        
        class_cluster = self.cluster2taste.index[idx_cluster]
        condition_cluster = self.df_whisky.Cluster == class_cluster
        df_cluster = self.df_whisky[condition_cluster]
        
        return class_cluster, df_cluster

    def filter_by_price(self, df_cluster, _price_min, _price_max):            
        return filter_by_price(self.CONFIG, df_cluster, _price_min, _price_max)
    
    def sort_by_popularity(self, df_cluster, topk=None):
        sort_by = self.CONFIG['sort_by']
        
        if topk:
            return df_cluster.sort_values(by=sort_by).iloc[:topk, :]
        else:
            return df_cluster.sort_values(by=sort_by)
        
        
class model_rec():
    def __init__(self,CONFIG,config, model, dataset, dataloader:UserDataLoader=None, goods:list=[], poors:list=[], user_id:str=None) -> None:
        self.goods = goods
        self.poors = poors
        self.user_id = user_id

        self.CONFIG=CONFIG

        self.config=config
        self.model=model
        self.dataset=dataset

        if dataloader:
            self.dataloader = dataloader
    
    def _recvae_predict(self) -> torch.Tensor:
        uid_series_good = self._encode(self.goods)
        uid_series_poor = self._encode(self.poors)
        
        rating_matrix = self._make_rating_matrix(uid_series_good)
        scores, _, _, _ = self.model.forward(rating_matrix, self.model.dropout_prob)

        # [PAD], self.goods, self.poors에 해당하는 모든 아이템 제외
        scores[:, 0] = -np.inf
        scores[:, uid_series_good] = -np.inf
        scores[:, uid_series_poor] = -np.inf
        
        return scores
    
    def _recvae_topk(self, k:int=10) -> tuple:
        scores = self._recvae_predict()
        topk_scores, topk_index = torch.topk(scores, k)
        return self._decode(topk_index.cpu()).tolist()[0]
    
    def _recvae_topk_filtered_by_Cost(self, k:int=10, _price_min:int=0, _price_max:int=1000000) -> tuple:
        scores = self._recvae_predict()[0]
        
        list_index_val = sorted(enumerate(scores.cpu()), key=lambda x: -x[1])
        tuple_idx_of_predict = list(zip(*list_index_val))[0]
        tuple_idx_of_predict = list(tuple_idx_of_predict)
        iterator = (i for i in self._decode(tuple_idx_of_predict))
        
        df_feature = pd.read_csv(self.CONFIG['dir_source_of_item'], sep=self.CONFIG['sep_source'], index_col='Whiskey')
        list_cost_allowed = filter_Cost_by_price(self.CONFIG, _price_min, _price_max)
        
        list_model_rec = []
        for whiskey in iterator:
            
            whiskey = whiskey.replace('ä', 'a')
            whiskey = whiskey.replace('é', 'e')
            if whiskey=='[PAD]':continue
            
            if len(list_model_rec) == k:
                break
            if not df_feature.loc[whiskey].Cost in list_cost_allowed:
                continue
            list_model_rec.append(whiskey)
        return list_model_rec
    
    # ##########################
    # 내부적으로만 사용되는 함수들
    def _make_rating_matrix(self, uid_series:np.ndarray) -> torch.Tensor:
        n_items = self.dataset.num(self.dataset.iid_field)
        device=self.config['device']
        
        col_indices = torch.Tensor(uid_series).to(device).long()
        row_indices = torch.zeros_like(col_indices).to(device).long()
        cell_values = torch.tensor(1.).to(device)
        
        rating_matrix = torch.zeros(1).to(device).repeat(1, n_items)
        rating_matrix.index_put_((row_indices, col_indices), cell_values)
        
        return rating_matrix
    
    def _encode(self, item:list) -> np.ndarray:
        return self.dataset.token2id(self.dataset.iid_field, item)
    
    def _encode_user(self, user:list) -> np.ndarray:
        return self.dataset.token2id(self.dataset.uid_field, user)
    
    def _decode(self, array_id:list) -> np.ndarray:
        return self.dataset.id2token(self.dataset.iid_field, array_id)

# %%
