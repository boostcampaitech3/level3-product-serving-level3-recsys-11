from re import I
from fastapi import FastAPI, UploadFile, File,Request
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any

from datetime import datetime

from recbole.quick_start.quick_start import load_data_and_model
import yaml
from pathlib import Path

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('Model'))))

from Model.utils import initiate,Collector,Greeter
from Model.train import train

app = FastAPI()
with open('Model/config.yaml', 'r') as f:
        CONFIG = yaml.safe_load(f)
# train(CONFIG)
config, model, dataset, dataloader, _, _=initiate(CONFIG)


@app.get("/")
def hello_world():
    return {"hello": "world"}


class Whiskey(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    info_link: str
    image_link: str

class Rec_lists(BaseModel):
    userid: UUID = Field(default_factory=uuid4)
    Whiskies: List[Whiskey] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # @property
    def add_product(self, item: Whiskey):
        self.Whiskies.append(item)
        self.updated_at = datetime.now()
        return self


rec_random = []
@app.get("/recommend_e_list", description="Expert 추천 리스트를 가져옵니다")
async def get_rec_random() -> List[Whiskey]:
    return rec_random

@app.post("/recommend_e", description="Expert 추천을 요청합니다.")
async def make_rec_random(item:Request):
    item_dict = await item.json()
    topk = item_dict['topk']
    whiskies_like = item_dict['whiskies']
    whiskies_hate = item_dict['whiskies']
    
    agent = Collector(whiskies_like,whiskies_hate)
    list_pop = agent._popularity(topk)
    list_recvae = agent._recvae_topk(topk)
    return list_recvae
    
@app.get("/recommend_b_list", description="Beginner 추천 리스트를 가져옵니다")
async def get_rec_random() -> List[Whiskey]:
    return rec_random

@app.post("/recommend_b", description="Beginner 추천을 요청합니다.")
async def make_rec_random(item:Request):
    item_dict = await item.json()
    topk = item_dict['topk']
    dict_taste = item_dict['dict_taste']
    agent = Greeter()
    result_orga = agent._cal_cos_sim(dict_taste, organized=True)
    result_cluster, result_df_cluster = agent.find_cluster(dict_taste)
    result_sort_by_popularity = agent.sort_by_popularity(result_df_cluster, topk=topk)
#     







