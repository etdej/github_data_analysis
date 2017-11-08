import collections as col
import gzip
import json
import os
import pandas as pd
import urllib.request

import specs
import utils
import shutil


def download_extract_save(base_path, url):
    """ Very dense "do-everything" function """
    raw_data_ls = get_raw_data(url)
    output = extract_data(raw_data_ls)
    date_str = url.split("/")[-1].replace(".json.gz", "")
    output_path = os.path.join(base_path, date_str)
    save_csvs(output, output_path)
    utils.save_fol_to_gzip(output_path + ".tar.gz", output_path)
    shutil.rmtree(output_path)


def get_raw_data(url):
    raw_data_ls = []
    request = urllib.request.Request(
        url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
        })
    response = urllib.request.urlopen(request)
    gzip_file = gzip.GzipFile(fileobj=response, mode="r")
    for line in gzip_file.readlines():
        raw_data_ls.append(json.loads(line))
    return raw_data_ls


def collect_specs(nested_dictionary, spec_ls):
    main_datum = dict()
    spec_error_ls = []
    for spec in spec_ls:
        spec_name = ".".join(spec)
        try:
            main_datum[spec_name] = utils.chain_ix(nested_dictionary, spec)
        except (KeyError, TypeError):
            main_datum[spec_name] = None
            spec_error_ls.append(spec_name)
    return main_datum, spec_error_ls


def extract_data_from_raw_data(raw_data_ls, event_extract_def):
    main_data = []
    all_errors = []
    repo_data = []
    event_i = 0
    for raw_i, raw_datum in enumerate(raw_data_ls):
        if raw_datum["type"] != event_extract_def["type"]:
            continue
        main_datum, spec_error_ls = collect_specs(
            nested_dictionary=raw_datum,
            spec_ls=event_extract_def["spec_ls"],
        )
        for repo_loc in event_extract_def["repo_loc_ls"]:
            try:
                repo_datum, repo_error_ls = collect_specs(
                    nested_dictionary=utils.chain_ix(raw_datum, repo_loc),
                    spec_ls=specs.REPO_SPEC_LS,
                )
                repo_data.append(repo_datum)
                spec_error_ls += repo_error_ls
            except (KeyError, TypeError):
                spec_error_ls.append(".".join(repo_loc))
        for spec_name in spec_error_ls:
            all_errors.append({
                "id": raw_datum.get("id"),
                "raw_i": raw_i,
                "event_i": event_i,
                "spec": spec_name,
            })
        main_data.append(main_datum)
        event_i += 1

    return {
        "data": pd.DataFrame(main_data),
        "errors": pd.DataFrame(all_errors),
        "repo": pd.DataFrame(repo_data),
    }


def extract_data(raw_data_ls):
    extracted_dict = col.OrderedDict()
    for event_extract_def in specs.EVENT_EXTRACTION_DEF_LS:
        extracted_dict[event_extract_def["type"]] = \
            extract_data_from_raw_data(
                raw_data_ls=raw_data_ls,
                event_extract_def=event_extract_def,
            )
    return extracted_dict


def save_csvs(data_output, output_fol):
    os.makedirs(output_fol, exist_ok=True)
    save_path_ls = []
    for event_type, event_dict in data_output.items():
        for key, df in event_dict.items():
            save_path = os.path.join(output_fol, f"{event_type}-{key}.csv")
            df.to_csv(save_path)
            save_path_ls.append(save_path)
    return save_path_ls


#def save_csvs_and_gzip(data_output, remove_csvs=False):



def load_csvs(output_fol):
    data_dict = col.OrderedDict()
    for file_name in os.listdir(output_fol):
        if ".csv" not in file_name:
            continue
        df = pd.read_csv(os.path.join(output_fol, file_name), index_col=0)
        event_type, key = file_name.replace(".csv", "").split("-")
        if event_type not in data_dict:
            data_dict[event_type] = dict()
        data_dict[event_type][key] = df
    return data_dict







