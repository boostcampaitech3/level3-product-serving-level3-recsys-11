# %%
from recbole.quick_start import run_recbole

from pathlib import Path

import yaml
with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)

# %%
dir_config = Path("config")
name_dataset = CONFIG['name_dataset']

config_dict = {
    'epochs':CONFIG['epochs'],
    'train_batch_size':CONFIG['train_batch_size'],
    'eval_batch_size':CONFIG['eval_batch_size'],
}
config_file_list = ['whiskey_pairwise.yaml', 'common.yaml']
# config_file_list = ['whiskey_pointwise.yaml', 'common.yaml']

config_file_list = [dir_config / i for i in config_file_list]

# %%
# https://recbole.io/docs/user_guide/model_intro.html
run_recbole(dataset=name_dataset, model='RecVAE', config_file_list=config_file_list, config_dict=config_dict)

# %%
