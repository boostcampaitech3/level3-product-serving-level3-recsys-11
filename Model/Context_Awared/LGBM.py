# %%
from lightgbm import LGBMClassifier, early_stopping

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from dataset import TagWhiskeyInterDataset

from lightgbm import plot_importance
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


# %%
dataset = TagWhiskeyInterDataset(threshold=80).df_inter

items = dataset.loc[:,'whiskey':]
targets = dataset.loc[:,'rating']

X_train, X_valid, y_train, y_valid = train_test_split(items, targets, test_size=0.2)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, test_size=0.5)
lgbm = LGBMClassifier(n_estimators=4000)

# %%
lgbm.fit(X_train, X_train, early_stopping_rounds=50, eval_metric='logloss', eval_set=(X_valid, y_valid), verbose=True)

# %%
def eval_metrics(y, y_preds):
    acc = accuracy_score(y, y_preds)
    f1 = f1_score(y, y_preds)
    auc = roc_auc_score(y, y_preds)
    return acc, f1, auc

# %%
y_test_preds = lgbm.predict(X_test)
y_valid_preds = lgbm.predict(X_valid)

acc, f1, auc = eval_metrics(y_test, y_test_preds)
print(acc)
print(f1)
print(auc)
acc, f1, auc = eval_metrics(y_valid, y_valid_preds)
print(acc)
print(f1)
print(auc)

# %%
plot_importance(lgbm)

# %%
# inference
tastes = [0.1234, 1.0, 0.234, -0.345, 0.134, 0.45, 0.1645, -0.3453, -0.26275, -0.96785, 0.3453, 0.567, 0.947, -0.2346]

def make_all_items_w_tastes(tastes):
    df_all_items_w_tastes = pd.DataFrame([[i] + tastes for i in range(1125)])
    df_all_items_w_tastes.columns = ['whiskey', 'body', 'sweet', 'sherry', 'malt', 'aperitif',
       'smoky', 'pungent', 'fruity', 'honey', 'floral', 'spicy', 'medicinal', 'nutty', 'winey']

    return df_all_items_w_tastes

y_preds = lgbm.predict(make_all_items_w_tastes(tastes))
print(len(np.where(y_preds==1)[0]))

# %%
# rating 사용자 별 정규화
df_inter = pd.read_csv('/opt/ml/workspace/team_git/Dataset/user_whiskey_interaction_renamed.csv', sep='$')
avg = df_inter[['user', 'rating']].groupby('user').mean().to_dict()['rating']
std = df_inter[['user', 'rating']].groupby('user').std().fillna(0.0).to_dict()['rating']
df_inter['rating'] = df_inter.apply(lambda row: (row['rating'] - avg[row['user']])/(std[row['user']]+1e-6), axis=1)


# %%
