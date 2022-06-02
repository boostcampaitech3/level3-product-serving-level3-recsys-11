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
train(CONFIG)
# initiate(CONFIG)


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
@app.get("/recommend_random", description="추천 리스트를 가져옵니다")
async def get_rec_random() -> List[Whiskey]:
    return rec_random

@app.post("/recommend_random", description="랜덤 추천을 요청합니다")
async def make_rec_random(item:Request):
    item_dict = await item.json()
    topk = item_dict['topk']
    random_rec_movies = get_random_rec(topk)
    random_rec_movies.to_csv('temp.csv')
    # print(random_rec_movies)
    tmp=[]
    for i in range(topk):
        tmp.append(Whiskey(title=random_rec_movies['title'].iloc[i],
        poster_link=random_rec_movies['poster_link'].iloc[i],
        year=random_rec_movies['year'].iloc[i]
                    ))
    new_rec=Movies(movies=tmp)
    rec_random.append(new_rec)
    return new_rec
    
@app.post("/recommend", description="추천을 요청합니다")
async def make_rec(model,likedmovies,topk):
    s3_rec_movies = get_model_rec(
                    model,
                    likedmovies,
                    topk,
                )
    return s3_rec_movies

users = []

@app.get("/users", description="유저들의 정보를 가져옵니다.")
async def get_users() -> List[Movies]:
    return users

@app.get("/users/{usersid}", description="Order 정보를 가져옵니다")
async def get_order(usersid: UUID) -> Union[Movies, dict]:
    # order_id를 기반으로 order를 가져온다
    user = get_user_by_id(usersid=usersid)
    if not user:
        return {"message": "유저 정보를 찾을 수 없습니다"}
    return user



def get_user_by_id(userid: UUID) -> Optional[Movies]:
    return next((user for user in users if user.id == userid), None)
    # 제네레이터
    # iter, next 키워드로 검색
    # 제네레이터를 사용한 이유 : 메모리를 더 절약해서 사용할 수 있음
    # 이터레이터, 이터러블, 제네레이터 => 파이썬 면접에서 많이 나오는 소재. GIL
    # iter는 반복 가능한 객체에서 이터레이터를 반환
    # next는 이터레이터에서 값을 차례대로 꺼냄



