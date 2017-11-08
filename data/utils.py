import os
import tarfile


def chain_ix(nested_dictionary, key_ls):
    """ Chain index a nested dictionary """
    x = nested_dictionary
    for key in key_ls:
        x = x[key]
    return x


def save_fol_to_gzip(save_path, fol_path):
    with tarfile.open(save_path, "w:gz") as tar:
        tar.add(fol_path, arcname=os.path.basename(fol_path))
