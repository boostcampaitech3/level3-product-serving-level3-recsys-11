# %%
from recbole.quick_start import run_recbole

from pathlib import Path

import os
import shutil
import yaml


def train(CONFIG):
    dir_config = Path("Model/config")
    name_dataset = CONFIG['name_dataset']
    config_dict = {
        'epochs':CONFIG['epochs'],
        'train_batch_size':CONFIG['train_batch_size'],
        'eval_batch_size':CONFIG['eval_batch_size'],
    }
    config_file_list = ['whiskey_pairwise.yaml', 'common.yaml']
    config_file_list = [dir_config / i for i in config_file_list]
    # https://recbole.io/docs/user_guide/model_intro.html
    run_recbole(dataset=name_dataset, model='RecVAE', config_file_list=config_file_list, config_dict=config_dict)
    rename(CONFIG)

def rename(CONFIG):
    path=CONFIG['dir_model_saved']
    file_list = sorted_ls(path)
    shutil.copyfile(path+'/'+file_list[-1],path+"/model.pth")


def sorted_ls(path):
    mtime=lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


if __name__=='__main__':
    with open('Model/config.yaml', 'r') as f:
        CONFIG = yaml.safe_load(f)

        train(CONFIG)



