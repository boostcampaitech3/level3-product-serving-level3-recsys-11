# %%
from lightgbm import LGBMClassifier, early_stopping

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, plot_confusion_matrix

from dataset import TagWhiskeyInterDataset

from lightgbm import plot_importance
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd


# %%
# dataset = TagWhiskeyInterDataset(threshold=86).df_inter
instance = TagWhiskeyInterDataset(threshold=0.5)
dataset = instance.df_inter

items = dataset.loc[:,'whiskey':]
targets = dataset.loc[:,'rating']

X_train, X_valid, y_train, y_valid = train_test_split(items, targets, test_size=0.2)
X_valid, X_test, y_valid, y_test = train_test_split(X_valid, y_valid, test_size=0.5)
lgbm = LGBMClassifier(n_estimators=20000)

def class_ratio(y):
    return (y==1).sum() / len(y)

print(f'trainset ratio\t{class_ratio(y_train)}')
print(f'validset ratio\t{class_ratio(y_valid)}')
print(f'testset ratio\t{class_ratio(y_test)}')

# %%
lgbm.fit(X_train, y_train, early_stopping_rounds=50, eval_metric='logloss', eval_set=(X_valid, y_valid), verbose=True)

# %%
def eval_metrics(y, y_preds):
    acc = accuracy_score(y, y_preds)
    f1 = f1_score(y, y_preds)
    auc = roc_auc_score(y, y_preds)
    cfm = confusion_matrix(y, y_preds)
    return acc, f1, auc, cfm

# %%
y_test_preds = lgbm.predict(X_test)
y_valid_preds = lgbm.predict(X_valid)

acc, f1, auc, cfm = eval_metrics(y_test, y_test_preds)
print(acc)
print(f1)
print(auc)
sns.heatmap(cfm, annot=True, fmt="d", cmap="YlGnBu")

# %%
acc, f1, auc, cfm = eval_metrics(y_valid, y_valid_preds)
print(acc)
print(f1)
print(auc)
sns.heatmap(cfm, annot=True, fmt="d", cmap="YlGnBu")

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

idxs = np.where(y_preds)[0]
decoder = instance.decoder
whisky_rec_by_tag = [decoder[idx] for idx in idxs]

# %%
import joblib

joblib.dump(lgbm, 'model_saved/lgbm_cutline_point5_try_01.pkl')

# %%
lgbm = joblib.load('model_saved/lgbm_cutline_1.pkl')
# %%
