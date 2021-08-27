#!/usr/bin/env python3

import os
import shlex
import shutil
import subprocess


def extract_archive(dataset_archive, tmp_data_path):
    if not os.path.isfile(dataset_archive):
        return False

    dataset_ext = os.path.splitext(dataset_archive)[1]
    if dataset_ext != ".gz" and dataset_ext != ".tar":
        return False

    if os.path.isdir(tmp_data_path):
        shutil.rmtree(tmp_data_path, ignore_errors=True)
    os.makedirs(tmp_data_path)

    if dataset_ext == ".gz":
        tar_opt = "-xzf"
    else:
        tar_opt = "-xf"

    extract_cmd = ("tar {} {} -C {}").format(tar_opt, dataset_archive, tmp_data_path)

    subprocess.call(shlex.split(extract_cmd))

    return True


def tar_file(tar_path, tmp_path):
    tar_name = tar_path.split('/')[-1]
    if extract_archive(tar_path, tmp_path):
        print('extract ' + tar_name + 'successfully!')
    else:
        print("fail to extract " + tar_name)
