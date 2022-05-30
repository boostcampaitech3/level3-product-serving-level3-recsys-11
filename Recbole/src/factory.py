# %%
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# %%
# config
dir_src = Path('/opt/ml/workspace/src')
scaler = MinMaxScaler()

# %%
df_total = pd.read_csv(dir_src / 'total.csv', sep='$')
df_images = pd.read_csv(dir_src / 'images.csv', sep='$')
df_whiskey_cluster = pd.read_csv(dir_src / 'whiskey_cluster.csv')
df_whisky_w_tags = pd.read_csv(dir_src / 'whisky_w_tags.csv', index_col='Unnamed: 0')
df_interaction = pd.read_csv(dir_src / 'interaction.csv', sep='$')
df_integration = pd.DataFrame([])

# %%
df_total = df_total.drop_duplicates().reset_index(drop=True)
df_images = df_images.drop_duplicates().reset_index(drop=True)
df_whiskey_cluster = df_whiskey_cluster.drop_duplicates().reset_index(drop=True)
df_whisky_w_tags = df_whisky_w_tags.drop_duplicates().reset_index(drop=True)
df_interaction = df_interaction.drop_duplicates().reset_index(drop=True)

# %%
df_total['whiskey'] = df_total['links'].map(lambda x : x.rpartition('/')[-1])
df_total.drop(columns=['title', 'Unnamed: 0'], inplace=True)
df_total.columns = ['Whisky', 'links', 'whiskey']

df_images['whiskey'] = df_images['links'].map(lambda x : x.rpartition('/')[-1])
df_images.drop(columns=['links'], inplace=True)

df_whisky_w_tags = df_whisky_w_tags[['Whisky', 'Meta Critic', 'STDEV', '#', 'Super Cluster', 'Cluster', 'Country', 'Type']]

df_whiskey_cluster = df_whiskey_cluster.rename(columns={'Unnamed: 0':'Cluster'})
df_max, df_min = df_whiskey_cluster.iloc[:, 1:].max(axis=0), df_whiskey_cluster.iloc[:, 1:].min(axis=0)
df_whiskey_cluster.iloc[:, 1:] = (df_whiskey_cluster.iloc[:, 1:] - df_min) / (df_max - df_min)

df_whiskey_price = df_interaction[['whiskey', 'price']].drop_duplicates(subset='whiskey')
df_whiskey_price['price'] = df_whiskey_price['price'].map(lambda x: x.partition(' ')[-1]).astype(np.float16)

# %%
df_total = df_total.drop_duplicates('whiskey').reset_index(drop=True)
df_images = df_images.drop_duplicates('whiskey').reset_index(drop=True)
df_whisky_w_tags = df_whisky_w_tags.drop_duplicates('Whisky').reset_index(drop=True)

# %%
df_integration = df_whisky_w_tags.merge(df_total, on='Whisky', how='left').drop(columns=['Whisky'])
df_integration = df_integration[~df_integration['whiskey'].isnull()]
df_integration = df_integration.merge(df_images, on='whiskey', how='left')
df_integration = df_integration.merge(df_whiskey_price, on='whiskey', how='left')
df_integration = df_integration.merge(df_whiskey_cluster, on='Cluster', how='left')

cols_integration = ['whiskey', 'Meta Critic', 'STDEV', '#', 'Super Cluster', 
                    'Country', 'Type', 'price', 'links', 'image_links', 
                    'Cluster', 'body', 'sweet', 'sherry', 'malt', 'aperitif', 
                    'smoky', 'pungent', 'fruity', 'honey', 'floral', 'spicy', 
                    'medicinal', 'nutty', 'winey']

df_integration = df_integration[cols_integration]

# %%
if __name__ == '__main__':
    from IPython.display import display
    
    display(df_total.head(2))
    display(df_images.head(2))
    display(df_whiskey_cluster.head(2))
    display(df_whisky_w_tags.head(2))
    display(df_interaction.head(2))
    display(df_integration.head(2))
    
# %%
if __name__ == '__main__':
    from IPython.display import display
    
    print(len(df_total))
    print(len(df_images))
    print(len(df_whiskey_cluster))
    print(len(df_whisky_w_tags))
    print(len(df_interaction))
    print(len(df_integration))

# %%
root_src = Path('src_processed')
sep = '$'

df_total.to_csv(root_src / 'total.csv', index=False, sep=sep)
df_images.to_csv(root_src / 'images.csv', index=False, sep=sep)
df_whiskey_cluster.to_csv(root_src / 'whiskey_cluster.csv', index=False, sep=sep)
df_whisky_w_tags.to_csv(root_src / 'whisky_w_tags.csv', index=False, sep=sep)
df_interaction.to_csv(root_src / 'interaction.csv', index=False, sep=sep)
df_integration.to_csv(root_src / 'integration.csv', index=False, sep=sep)
# %%
