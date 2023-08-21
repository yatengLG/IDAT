# -*- coding: utf-8 -*-
# @Author  : LG
from collections import namedtuple
from json import dump, load
from typing import List, Dict
from xml.etree import ElementTree as ET
import os
import yaml

CATEGORYTUPLE = namedtuple('LABEL', ['category', 'color'])

def load_config(file):
    result = []
    with open(file, 'rb')as f:
        label = yaml.load(f.read(), Loader=yaml.FullLoader)['label']

    for d in label:
        category = d['name']
        color = d['color']
        label_tuple = CATEGORYTUPLE(category, color)
        result.append(label_tuple)

    return result

def save_config(labeltuple_list:List[CATEGORYTUPLE], file:str):
    cfg = {}
    cfg['label'] = []
    for cate, colo in labeltuple_list:
        cfg['label'].append({'name': cate, 'color': colo})
    s = yaml.dump(cfg)
    with open(file, 'w') as f:
        f.write(s)
    return True

def save_category_cfg(labeltuple_list:List[CATEGORYTUPLE], file:str):
    if file.endswith('.txt'):
        with open(file, 'w') as f:
            for labeltuple in labeltuple_list:
                f.write("{} {}\n".format(labeltuple.category, labeltuple.color))
        return True

    elif file.endswith('.json'):
        D = {}
        D['categorys'] = []
        for labeltuple in labeltuple_list:
            D['categorys'].append({'category': labeltuple.category,
                                   'color': labeltuple.color})
        with open(file, 'w') as f:
            dump(D, f, indent=4)

        return True
    else:
        return False

def read_category_cfg(file:str):
    result = []
    print(file)
    if file.endswith('.txt'):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line:str = line.rstrip('\n')
                category, color = line.split(' ')
                label_tuple = CATEGORYTUPLE(category, color)
                result.append(label_tuple)
        return result
    elif file.endswith('.json'):
        with open(file, 'r') as f:
            D = load(f)
            categorys = D['categorys']
            for category_color_dict in categorys:
                category, color = category_color_dict['category'], category_color_dict['color']
                label_tuple = CATEGORYTUPLE(category, color)
                result.append(label_tuple)
        return result
    else:
        return None

def annotation_count(label_root:str):
    record_dict = {}
    label_files = [f for f in os.listdir(label_root) if f.endswith('.xml')]
    for file in label_files:
        file = os.path.join(label_root, file)
        tree = ET.parse(file)
        objs = tree.findall('object')
        for obj in objs:
            name = obj.find('name').text
            is_difficult = bool(int(obj.find('difficult').text))
            if name not in record_dict:
                record_dict[name] = {'total_num':1, 'diff_num':int(is_difficult)}
            else:
                record_dict[name]['total_num'] += 1
                record_dict[name]['diff_num'] += int(is_difficult)
    return record_dict
