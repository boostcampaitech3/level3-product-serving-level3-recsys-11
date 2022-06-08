# %%
from recbole.utils.case_study import full_sort_scores, full_sort_topk
from recbole.quick_start.quick_start import load_data_and_model
from recbole.data.dataloader.user_dataloader import UserDataLoader

import pandas as pd
import numpy as np
import torch
from pathlib import Path

import yaml
with open('config.yaml', 'r') as f:
    CONFIG = yaml.load(f)

from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from sklearn.preprocessing import MinMaxScaler

from typing import Dict, List
from collections import defaultdict

from deprecated import deprecated

# %%
class Collector():
    def __init__(self, goods:list=[], poors:list=[], user_id:str=None, dataloader:UserDataLoader=None) -> None:
        self.goods = goods
        self.poors = poors
        self.user_id = user_id
        self.config, self.model, self.dataset, self.dataloader, _, _ = load_data_and_model(
            model_file=Path(CONFIG['dir_model_saved']) / CONFIG['file_model_used'],
        )
        self.config_vae, self.model_vae, _, _, _, _ = load_data_and_model(
            model_file=Path(CONFIG['dir_model_saved']) / CONFIG['file_model_vae_used'],
        )
        if dataloader:
            self.dataloader = dataloader
    
    def topk(self, k:int=10) -> list:
        return self._popularity(k)
    
    def retrain(self) -> None:
        raise NotImplementedError
    
    def _popularity(self, k:int=10) -> list:
        list_pop = []
        dir_Pop = Path(CONFIG['dir_dataset']) / CONFIG['name_dataset'] / f'Pop.csv'
        iterator = pd.read_csv(dir_Pop).iterrows()
        
        for idx, row in iterator:
            whiskey = row['whiskey']
            if len(list_pop) == k:
                break
            if whiskey in self.goods:
                continue
            elif whiskey in self.poors:
                continue
            list_pop.append(whiskey)
        return list_pop
    
    def _recbole(self, k:int=10) -> list:
        uid_series = self._encode_user([self.user_id])
        
        topk_score, topk_iid_list = full_sort_topk(
            uid_series, self.model, 
            self.dataloader, k=k, 
            device=self.config['device'])
        
        return self._decode(topk_iid_list.cpu())[0]
    
    def _recvae_predict(self) -> torch.Tensor:
        uid_series_good = self._encode(self.goods)
        uid_series_poor = self._encode(self.poors)
        
        rating_matrix = self._make_rating_matrix(uid_series_good)
        scores, _, _, _ = self.model_vae.forward(rating_matrix, self.model_vae.dropout_prob)

        # [PAD], self.goods, self.poors에 해당하는 모든 아이템 제외
        scores[:, 0] = -np.inf
        scores[:, uid_series_good] = -np.inf
        scores[:, uid_series_poor] = -np.inf
        
        return scores
    
    def _recvae_topk(self, k:int=10) -> tuple:
        scores = self._recvae_predict()
        topk_scores, topk_index = torch.topk(scores, k)
        return self._decode(topk_index.cpu()).tolist()[0]
    
    # ##########################
    # 내부적으로만 사용되는 함수들
    def _make_rating_matrix(self, uid_series:np.ndarray) -> torch.Tensor:
        n_items = self.dataset.num(self.dataset.iid_field)
        device=self.config_vae['device']
        
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
class Greeter():
    def __init__(self) -> None:
        self.df_whisky = pd.read_csv(CONFIG['dir_integration'], sep=CONFIG['sep_source'])
        self.cluster2taste = pd.read_csv(CONFIG['dir_whiskey_cluster'], sep=CONFIG['sep_source'])
        self.cluster2taste = self.cluster2taste.set_index('Cluster')
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
        if _price_min > _price_max:
            tmp = _price_min
            _price_min = _price_max
            _price_max = tmp
        
        idx_min = self._find_idx_range_cost(_price_min)
        idx_max = self._find_idx_range_cost(_price_max)
        
        list_price_allowed = self.list_cost[idx_min:idx_max+1]
        
        condition = df_cluster.Cost.isin(list_price_allowed)
        return df_cluster[condition]
    
    @deprecated(reason='데이터셋이 바뀜.')
    def filter_by_price_class(self, df_cluster, _price_min, _price_max):            
        if _price_min > _price_max:
            tmp = _price_min
            _price_min = _price_max
            _price_max = tmp
        
        condition = (_price_min <= df_cluster.price) & (df_cluster.price < _price_max)
        return df_cluster[condition]

    def _find_idx_range_cost(self, val):
        won_per_cad = CONFIG['won_per_cad']
        val = val / won_per_cad
        
        for idx, (k, (v_min, v_max)) in enumerate(self.dict_range_cost.items()):
            if v_min <= val < v_max:
                return idx
        raise IndexError
    
    def sort_by_popularity(self, df_cluster, topk=None):
        sort_by = CONFIG['sort_by']
        
        if topk:
            return df_cluster.sort_values(by=sort_by).iloc[:topk, :]
        else:
            return df_cluster.sort_values(by=sort_by)

# %%
if __name__ == '__main__':
    from IPython.display import display
    
    # 인스턴스 생성 시, 좋아하는 위스키 목록과 싫어하는 위스키 목록 전달.
    agent = Collector(['Macallan 10yo Full Proof 57% 1980 (OB, Giovinetti & Figli)', "Jura 16yo Diurach's Own"], ['BenRiach Birnie Moss'])
    
    # 해당 목록을 기준으로 '인기도 기반 추천 목록'과 'VAE 기반 알고리즘 추천 목록' 전달.
    list_pop = agent._popularity(10)
    list_recvae = agent._recvae_topk(10)
    print(f"list_pop : \n{list_pop}")
    print(f"list_recvae : \n{list_recvae}")

# %%
if __name__ == '__main__':
    from IPython.display import display
    
    # 인스턴스 생성 및 사용자의 취향을 설정.
    agent = Greeter()
    dict_taste = {'body':2, 'sweet':5, 'sherry':0}
    
    # 코사인 거리를 각 클러스터 별로 계산
    result_orga = agent._cal_cos_sim(dict_taste, organized=True)
    print(result_orga)
    
    # 가장 유사도가 높은 클러스터를 'A'와 같이 출력
    # 해당 클러스터에 해당하는 DataFrame을 출력
    result_cluster, result_df_cluster = agent.find_cluster(dict_taste)
    print(result_cluster)
    display(result_df_cluster)
    
    # 원화 가격 기준으로 가격을 필터링한 DataFrame을 출력
    result_filter_by_price = agent.filter_by_price(result_df_cluster, 125000, 500000)
    display(result_filter_by_price)
    
    # 인기도 기준으로 정렬된 DataFrame을 출력
    # topk를 설정한 경우 k개만 출력
    result_sort_by_popularity = agent.sort_by_popularity(result_df_cluster, topk=10)
    display(result_sort_by_popularity)
    
    
# %%
