import collections as col
import gzip
import json
import pandas as pd
import urllib.request

import specs


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
            main_datum[spec_name] = chain_ix(nested_dictionary, spec)
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
                repo_datum = collect_specs(
                    nested_dictionary=chain_ix(raw_datum, repo_loc),
                    spec_ls=specs.REPO_SPEC_LS,
                )
                repo_data.append(repo_datum)
            except (KeyError, TypeError):
                spec_error_ls.append(repo_loc)
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


def chain_ix(nested_dictionary, key_ls):
    """ Chain index a nested dictionary """
    x = nested_dictionary
    for key in key_ls:
        x = x[key]
    return x

