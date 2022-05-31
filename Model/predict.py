from anyio import open_file
from recbole.quick_start.quick_start import load_data_and_model
from recbole.quick_start import run_recbole
from recbole.utils.case_study import full_sort_scores, full_sort_topk
from pathlib import Path
from glob import glob
from shutil import copytree, ignore_patterns
import yaml

def get_random_rec(top_k,config):
    return 0

def get_model_rec(model, config_path,top_k):
    config, model, dataset, train_data, valid_data, test_data=load_model(config_path,top_k)

    uid_series = dataset.token2id(dataset.uid_field, ['whiskycuse', 'Nopax'])
    topk_score, topk_iid_list = full_sort_topk(uid_series, model, test_data, k=10, device=config['device'])
    external_item_list = dataset.id2token(dataset.iid_field, topk_iid_list.cpu())

    return external_item_list

def load_model(config_path,top_k):
    with open(config_path) as f:
        CONFIG = yaml.load(f)

    dir_model_saved = Path(CONFIG['dir_model_saved'])
    file_model_used = CONFIG['file_model_used']

    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
    model_file=dir_model_saved / file_model_used,)

    return config, model, dataset, train_data, valid_data, test_data

def train_model(config_path):
    with open('config.yaml', 'r') as f:
        CONFIG = yaml.safe_load(f)

    dir_config = Path("config")
    name_dataset = CONFIG['name_dataset']

    config_dict = {
    'epochs':CONFIG['epochs'],
    'train_batch_size':CONFIG['train_batch_size'],
    'eval_batch_size':CONFIG['eval_batch_size'],
    }
    config_file_list = ['whiskey_pairwise.yaml', 'common.yaml']

    config_file_list = [dir_config / i for i in config_file_list]

    run_recbole(dataset=name_dataset, model='RecVAE', config_file_list=config_file_list, config_dict=config_dict)
    
    return 0
