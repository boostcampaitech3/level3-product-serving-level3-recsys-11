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

import pandas as pd
app = FastAPI()
with open('Model/config.yaml', 'r') as f:
        CONFIG = yaml.safe_load(f)

# train(CONFIG)
config, model, dataset, dataloader, _, _=initiate(CONFIG)

total_df=pd.read_csv(CONFIG['dir_integration'],sep="$")
@app.get("/")
def hello_world():
    return {"hello": "world"}


class Whiskey(BaseModel):
    name: str
    info_link: str
    image_link: str

class Rec_lists(BaseModel):
    userid: UUID = Field(default_factory=uuid4)
    popularity: List[Whiskey] = Field(default_factory=list)
    model: List[Whiskey] = Field(default_factory=list)
    tag: List[Whiskey] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)





@app.post("/recommend_e", description="Expert 추천을 요청합니다.")
async def make_rec_random(item:Request):
    item_dict = await item.json()

    whiskies_like = item_dict['whiskies_like']
    whiskies_hate = item_dict['whiskies_hate']
    topk = item_dict['topk']
    agent = Collector(CONFIG,config, model, dataset, dataloader,whiskies_like,whiskies_hate)
    df_pop = agent._popularity(topk)
    df_recvae = agent._recvae_topk(topk)
    pop,recvae=[],[]
    for i in range(topk):
        condition=total_df.Whiskey==df_pop[i]

        pop.append(
        Whiskey(name=total_df[condition].Whiskey.iloc[0],
        info_link=total_df[condition].links.iloc[0],
        image_link=total_df[condition].images.iloc[0])
        )

        condition=total_df.Whiskey==df_recvae[i]

        recvae.append(
        Whiskey(name=total_df[condition].Whiskey.iloc[0],
        info_link=total_df[condition].links.iloc[0],
        image_link=total_df[condition].images.iloc[0])
        )
    result=Rec_lists(popularity=pop,model=recvae)

    return result
    

@app.post("/recommend_b", description="Beginner 추천을 요청합니다.")
async def make_rec_random(item:Request):
    item_dict = await item.json()

    tag_list = item_dict['tag_list']
    price_low=item_dict['price_low']
    price_high=item_dict['price_high']
    topk = item_dict['topk']
    
    agent = Greeter(CONFIG)
    df_pop = agent._popularity(topk)

    result_cluster, result_df_cluster = agent.find_cluster(tag_list)
    result_filter_by_price = agent.filter_by_price(result_df_cluster, price_low, price_high)
    result_sort_by_popularity = agent.sort_by_popularity(result_filter_by_price, topk=topk)

    df_tag_pop = result_sort_by_popularity.Whiskey.iloc
    
    pop,tags=[],[]
    for i in range(topk):
        condition=total_df.Whiskey==df_pop[i]

        pop.append(
        Whiskey(name=total_df[condition].Whiskey.iloc[0],
        info_link=total_df[condition].links.iloc[0],
        image_link=total_df[condition].images.iloc[0])
        )

        condition=total_df.Whiskey==df_tag_pop[i]

        tags.append(
        Whiskey(name=total_df[condition].Whiskey.iloc[0],
        info_link=total_df[condition].links.iloc[0],
        image_link=total_df[condition].images.iloc[0])
        )
    result=Rec_lists(popularity=pop,tag=tags)
    return result
#     







