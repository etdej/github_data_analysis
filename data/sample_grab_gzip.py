import urllib.request
import gzip
import json


def get_data(url):
    data_ls = []
    request = urllib.request.Request(
        url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
        })
    response = urllib.request.urlopen(request)
    gzipFile = gzip.GzipFile(fileobj=response, mode="r")
    for line in gzipFile.readlines():
        data_ls.append(json.loads(line))
    return data_ls


if __name__ == "__main__":
    data_ls = get_data("http://data.githubarchive.org/2015-03-01-15.json.gz")
    print(len(data_ls))
