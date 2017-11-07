import pandas as pd

import grab_data

url = 'http://data.githubarchive.org/2015-05-22-12.json.gz'
raw_data_ls = grab_data.get_raw_data(url)
output = grab_data.extract_data(raw_data_ls)

print(pd.DataFrame({
    k1: {k2: len(v2) for k2, v2 in v1.items()}
    for k1, v1 in output.items()
}).T)
