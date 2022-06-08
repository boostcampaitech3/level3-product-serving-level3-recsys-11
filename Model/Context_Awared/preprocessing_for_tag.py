# %%
import numpy as np
import pandas as pd


# %%
df_whisky_w_tag = pd.read_csv('/opt/ml/workspace/team_git/Dataset/whiskey_w_tags_norm.csv', sep='$')
df_whisky_w_tag = df_whisky_w_tag.drop(['Meta Critic', 'STDEV', '#', 'Cost', 'Class', 'Super Cluster', 'Cluster'], axis=1)

# %%
df_inter = pd.read_csv('/opt/ml/workspace/team_git/Dataset/user_whiskey_interaction_renamed.csv', sep='$')
df_inter = df_inter.drop(['price', 'url'], axis=1)

# rating 사용자 별 정규화
avg = df_inter[['user', 'rating']].groupby('user').mean().to_dict()['rating']
std = df_inter[['user', 'rating']].groupby('user').std().fillna(0.0).to_dict()['rating']
df_inter['rating'] = df_inter.apply(lambda row: (row['rating'] - avg[row['user']])/(std[row['user']]+1e-6), axis=1)


# %%
df_tag_inter = df_inter.merge(df_whisky_w_tag, how='left', left_on='whiskey', right_on='Whiskey')
df_tag_inter = df_tag_inter.drop(['Whiskey', 'whiskey', 'rating'], axis=1)

# %%
df_user_replaced_by_tag = df_tag_inter.groupby('user').mean()

# %%
df_tag_whiskey_interaction = df_inter.merge(df_user_replaced_by_tag, how='left', on='user')
df_tag_whiskey_interaction.drop('user', axis=1, inplace=True)

# %%
df_iid = df_tag_whiskey_interaction[['whiskey']]\
    .drop_duplicates()\
        .reset_index(drop=True)
df_iid.index.name = 'iid'

# %%
# df_user_replaced_by_tag.to_csv('/opt/ml/workspace/team_git/Dataset/user_taste_avg.csv', index=True)
df_tag_whiskey_interaction.to_csv('/opt/ml/workspace/team_git/Dataset/tag_whiskey_interaction_norm.csv', index=False)
# df_iid.to_csv('/opt/ml/workspace/team_git/Dataset/whiskey_id.csv', index=True)

# %%
