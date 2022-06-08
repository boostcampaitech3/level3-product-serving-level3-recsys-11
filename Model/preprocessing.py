# %%
import pandas as pd
from pathlib import Path

import yaml
with open('config.yaml', 'r') as f:
    CONFIG = yaml.load(f)


# %%
columns_inter       = CONFIG['columns_inter']
columns_inter_types = CONFIG['columns_inter_types']

columns_item        = CONFIG['columns_item']
columns_item_types  = CONFIG['columns_item_types']

sep         = '\t'
sep_source  = CONFIG['sep_source']

col_user  = CONFIG['col_user']
col_item  = CONFIG['col_item']

name_dataset    = CONFIG['name_dataset']
dir_dataset    = Path(CONFIG['dir_dataset'])

dir_source_of_interaction = CONFIG['dir_source_of_interaction']
dir_source_of_item = CONFIG['dir_source_of_item']
dir_inter = dir_dataset / name_dataset / f'{name_dataset}.inter'
dir_item = dir_dataset / name_dataset / f'{name_dataset}.item'
dir_Pop = dir_dataset / name_dataset / f'Pop.csv'

# %%
# .inter 생성을 위한 cell
df_source_of_interaction = pd.read_csv(dir_source_of_interaction, sep=sep_source)
df_inter = df_source_of_interaction[columns_inter]

columns_inter_with_types = [f"{col}:{_type}" for col, _type in zip(columns_inter, columns_inter_types)]
df_inter.columns = columns_inter_with_types

# %%
# .inter 생성을 위한 cell
df_inter.to_csv(dir_inter, index=False, sep=sep)

# %%
# .item 생성을 위한 cell
df_source_of_item = pd.read_csv(dir_source_of_item, sep=sep_source)
df_item = df_source_of_item[columns_item]

columns_item_with_types = [f"{col}:{_type}" for col, _type in zip(columns_item, columns_item_types)]
df_item.columns = columns_item_with_types

# %%
# .item 생성을 위한 cell
df_item.to_csv(dir_item, index=False, sep=sep)

# %%
# 데이터 인기도순 추천을 위한 전처리 과정
df_pop = df_source_of_interaction[[col_user, col_item]]\
    .groupby(col_item).count()\
        .sort_values(col_user, ascending=False)\
            .reset_index()

# %%
# 데이터 인기도순 추천을 위한 전처리 과정
df_pop.to_csv(dir_Pop, index=False)

# %%
