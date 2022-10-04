import tarfile
import glob
import os
import pandas as pd
import datetime as dt
import shutil


CSV_LS = [
    f"{event_type}-{data_type}.csv"
    for event_type in [
        "CreateEvent", "ForkEvent", "IssueCommentEvent", "IssuesEvent",
        "MemberEvent", "PullRequestEvent", "PullRequestReviewCommentEvent",
        "PushEvent", "WatchEvent",
    ]
    for data_type in ["data", "errors", "repo"]
]


def get_datetime(path):
    return dt.datetime(*map(int, path.split("/")[-1].split(".")[0].split("-")))


def roll_up_hourly_data_to_daily(hourly_fol, temp_fol, daily_fol):
    # Get DF of tars
    tar_ls = glob.glob(os.path.join(hourly_fol, "*/*.tar.gz"))
    df = pd.DataFrame({"path": tar_ls})
    df.index = df["path"].apply(get_datetime)
    df = df.sort_index()
    df["date"] = df.index.normalize()

    # Group-by date, extract and concat, save
    for ts, path_srs in df["path"].groupby(df["date"]):
        print(ts)
        for path in path_srs:
            with tarfile.open(path) as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar, temp_fol)

        day_str = ts.strftime("%Y-%m-%d")
        day_fol = os.path.join(temp_fol, day_str)
        os.makedirs(day_fol, exist_ok=True)
        for csv_filename in CSV_LS:
            csv_df_ls = []
            for path in path_srs:
                extracted_fol = path.split("/")[-1].replace(".tar.gz", "")
                csv_df_ls.append(pd.read_csv(
                    os.path.join(temp_fol, extracted_fol, csv_filename),
                    index_col=0,
                ))
            combined_df = pd.concat(csv_df_ls).reset_index(drop=True)
            combined_df.to_csv(os.path.join(temp_fol, day_fol, csv_filename))

        with tarfile.open(os.path.join(daily_fol, day_str) + ".tar.gz", "w:gz") \
                as tar:
            tar.add(day_fol, arcname=os.path.basename(day_fol))

        shutil.rmtree(temp_fol)
        os.makedirs(temp_fol)


if __name__ == "__main__":
    roll_up_hourly_data_to_daily(
        hourly_fol="/home/zphang/data/github/hourly/",
        temp_fol="/home/zphang/data/github/temp",
        daily_fol="/home/zphang/data/github/daily",
    )