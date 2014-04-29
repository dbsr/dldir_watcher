# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import os
import time
import subprocess
import json
from contextlib import contextmanager
from argparse import ArgumentParser

from persistent import persistent_data

persistent_data_fpath = '/tmp/dldir_watcher.json~'




@contextmanager
def persistent_data():
    if not os.path.exists(persistent_data_fpath):
        data = {}
    else:
        with open(config.persistent_data_fpath, 'r') as f:
            data = json.load(f)
    yield data
    with open(persistent_data_fpath, 'w') as f:
        json.dump(data, f)


def fp_listdir(dpath):
    return [os.path.join(dpath, f) for f in os.listdir(dpath)]


def scan_directory(directory, script):
    with persistent_data() as data:
        if not data.get('skip_files'):
            data['skip_files'] = []
        skip_files = [str(f.encode('utf8', 'replace')) for f in data['skip_files']]
        for fpath in fp_listdir(directory):
            if fpath not in skip_files:
                data['skip_files'].append(fpath.decode('utf8'))
                subprocess.Popen(script.split() + [fpath])
        data['skip_files'] = filter(
            lambda fpath: os.path.exists(fpath),
            data['skip_files'])


def expand_user_path(argpath):
    return ' '.join([os.path.expanduser(p) for p in argpath.split()])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--directory', '-d', type=expand_user_path, help='full path to target directory')
    parser.add_argument('--script', '-s', type=expand_user_path, help='eg. python ~/proc.py')
    args = vars(parser.parse_args())
    scan_directory(**args)

