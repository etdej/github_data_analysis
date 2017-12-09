import pandas as pd
import numpy as np
import tarfile
import tqdm
import os
import shutil
from functools import reduce


def preprocess_file(path, verbose=False, final_type=np.uint64):
    ## PullRequest
    data = pd.read_csv(path+'PullRequestEvent-data.csv', index_col='Unnamed: 0')

    pr_closed_count = data[data['payload.action'] == 'closed'].groupby('repo.id').count().iloc[:, [1]]
    pr_closed_count.columns = ['pr_closed_count']

    pr_opened_count = data[data['payload.action'].isin(['opened', 'reopened'])].groupby('repo.id').count().iloc[:, [1]]
    pr_opened_count.columns = ['pr_opened_count']

    ## Pull request Comments
    data  = pd.read_csv(path+'PullRequestReviewCommentEvent-data.csv', index_col='Unnamed: 0')

    comment_pr_count = data[data['payload.action'] == 'created'].groupby('repo.id').count().iloc[:, [1]]
    comment_pr_count.columns = ['comment_pr_count']

    #comment_by_owner_count = data[data['payload.action'] == ['created'] & ].groupby('repo.id').count().iloc[:, [1]]
    
    ## Comments
    data  = pd.read_csv(path+'IssueCommentEvent-data.csv', index_col='Unnamed: 0')
    comment_issue_count = data[data['payload.action'] == 'created'].groupby('repo.id').count().iloc[:, [1]]
    comment_issue_count.columns = ['comment_pr_count']
    
    ## Push
    data  = pd.read_csv(path+'PushEvent-data.csv', index_col='Unnamed: 0')

    push_count = data.groupby('repo.id').count().iloc[:, [1]]
    push_count.columns = ['push_count']

    total_push_size = data[['repo.id', 'payload.size']].groupby('repo.id').sum()
    total_push_size.columns = ['total_push_size']

    ## Forks
    data  = pd.read_csv(path+'ForkEvent-data.csv', index_col='Unnamed: 0')
    fork_count = data.groupby('repo.id').count().iloc[:, [1]]
    fork_count.columns = ['fork_count']

    ## Issues
    data  = pd.read_csv(path+'IssuesEvent-data.csv', index_col='Unnamed: 0')

    issue_closed_count = data[data['payload.action'] == 'closed'].groupby('repo.id').count().iloc[:, [1]]
    issue_closed_count.columns = ['issue_closed_count']

    issue_opened_count = data[data['payload.action'].isin(['opened', 'reopened'])].groupby('repo.id').count().iloc[:, [1]]
    issue_opened_count.columns = ['issue_opened_count']

    # Watch
    data  = pd.read_csv(path+'WatchEvent-data.csv', index_col='Unnamed: 0')

    new_watch_count = data[data['payload.action'] == 'started'].groupby('repo.id').count().iloc[:, [1]]
    new_watch_count.columns = ['new_watch_count']

    # Create
    data  = pd.read_csv(path+'CreateEvent-data.csv', index_col='Unnamed: 0')

    new_branch_count = data[data['payload.ref_type'] == 'branch'].groupby('repo.id').count().iloc[:, [1]]
    new_branch_count.columns = ['new_branch_count']

    new_tag_count = data[data['payload.ref_type'] == 'tag'].groupby('repo.id').count().iloc[:, [1]]
    new_tag_count.columns = ['new_tag_count']


    ## Merging everything
    dfs = [pr_closed_count, pr_opened_count, comment_pr_count, push_count, total_push_size, 
           fork_count, issue_closed_count,issue_opened_count, new_watch_count, new_branch_count, new_tag_count]


    df_final = reduce(lambda left,right: pd.merge(left,right,how='outer', left_index=True, right_index=True).fillna(0), dfs)

    df_final[:] = df_final[:].astype(final_type)

    if verbose:
        print(df_final.info())

    return df_final


def extract_preprocess_save(date, path, out_path, mode):
    assert mode in ["csv", "pickle"]
    output_file_path = out_path + date + f'.{mode}'

    if os.path.exists(output_file_path): return
    tmp = "/tmp/"
    tar_path = path + date + ".tar.gz"
    with tarfile.open(tar_path) as tar:
        tar.extractall(tmp)
    extracted_path = tmp + date + "/"
    df = preprocess_file(extracted_path, verbose=False, final_type=np.uint64)
    if mode == "csv":
        df.to_csv(output_file_path)
    else:
        df.astype("int32").to_pickle(output_file_path)
    shutil.rmtree(extracted_path)


def preprocess(start_date, end_date, path, out_path, mode="csv"):
    dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(start_date, end_date)]
    for date in tqdm.tqdm(dates):
        extract_preprocess_save(date, path, out_path, mode=mode)


if __name__ == "__main__":
    import time
    t1 =time.time()
    preprocess('2015-02-01', '2015-02-01', "/Users/etienne/Dropbox/NYU/DS-GA1001-IntroToDSc/project/sample_data/", "out/")
    t2 = time.time()
    print(t2 - t1)
