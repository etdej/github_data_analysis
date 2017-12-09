from functools import reduce
import collections as col
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

FIELD_NAMES = [
    'pr_closed_count',
    'pr_opened_count',
    'comment_pr_count',
    'push_count',
    'total_push_size',
    'fork_count',
    'issue_closed_count',
    'issue_opened_count',
    'new_watch_count',
    'new_branch_count',
    'new_tag_count',
]

FIELD_NAMES_MAP = {
    'pr_closed_count': "# PRs Closed",
    'pr_opened_count': "# PRs Opened",
    'comment_pr_count': "# Comments on PRs",
    'push_count': "# Pushes",
    'total_push_size': "Total Push Size",
    'fork_count': "# New Forks",
    'issue_closed_count': "# Issues Closed",
    'issue_opened_count': "# Issues Opened",
    'new_watch_count': "# New Watches",
    'new_branch_count': "# Branches Created",
    'new_tag_count': "# Tags Created",
}


def select_latestmonth_data(df_data):
    col_latestmonth = [col_name for col_name in df_data.columns if "9" in col_name]
    df_latestmonth = df_data[col_latestmonth]
    return df_latestmonth


def select_all9months_data(data_df, year, start_month):
    """ Select 9-month Data with "fork count" and "new watch count" as target
    variables """
    selected_columns_timeless = []
    col_names_x = []
    i = 1
    for month in range(start_month, min(start_month + 9, 13)):
        selector_x = "{:}-{:02}".format(year, month)
        new_selected_columns_timeless = [col_name for col_name in
                                         data_df.columns if
                                         selector_x in col_name]
        col_names_x += [selected_col[:-7] + str(i) for selected_col in
                        new_selected_columns_timeless]
        selected_columns_timeless += new_selected_columns_timeless
        i += 1

    year += 1
    for month in range(1,
                       (start_month + 9) % 12 if (start_month + 9) > 13 else 0):
        selector_x = "{:}-{:02}".format(year, month)
        new_selected_columns_timeless = [col_name for col_name in
                                         data_df.columns if
                                         selector_x in col_name]
        col_names_x += [selected_col[:-7] + str(i) for selected_col in
                        new_selected_columns_timeless]
        selected_columns_timeless += new_selected_columns_timeless
        i += 1

    data_x = data_df[selected_columns_timeless]
    data_x.columns = col_names_x

    selector_y_forkcount = "fork_count_{:}-{:02}".format(
        year, start_month)
    col_name_y_forkcount = selector_y_forkcount[:-7] + str(12)

    data_y_forkcount = data_df[selector_y_forkcount]
    data_y_forkcount.columns = col_name_y_forkcount

    selector_y_newwatchcount = "new_watch_count_{:}-{:02}".format(
        year, start_month)
    col_name_y_newwatchcount = selector_y_newwatchcount[:-7] + str(12)

    data_y_newwatchcount = data_df[selector_y_newwatchcount]
    data_y_newwatchcount.columns = col_name_y_newwatchcount

    return data_x, data_y_forkcount, data_y_newwatchcount


def aux(left, right):
    return left + right


def generatecombineddataset(data_df, year, timerange_of_startingtime):
    """ Generate combined dataset for selected time range """
    dfs_x = []
    dfs_y_forkcount = []
    dfs_y_newwatchcount = []

    for monthselect in timerange_of_startingtime:
        df_x, df_y_forkcount, df_y_newwatchcount = select_all9months_data(
            data_df, year, monthselect)
        dfs_x.append(df_x)
        dfs_y_forkcount.append(df_y_forkcount)
        dfs_y_newwatchcount.append(df_y_newwatchcount)

    df_x_combined = pd.concat(dfs_x)
    df_y_combined_forkcount = pd.concat(dfs_y_forkcount)
    df_y_combined_newwatchcount = pd.concat(dfs_y_newwatchcount)

    return df_x_combined, df_y_combined_forkcount, df_y_combined_newwatchcount

"""
def crossvalscore(data_x, data_y):
    scores = []
    regr = linear_model.LinearRegression(normalize=True)
    scoremethods = ["r2", "neg_mean_squared_error"]
    for scoremethod in scoremethods:
        for time in range(10):
            X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.3)
            score = cross_val_score(regr, X_train, y_train, cv = 10, scoring = scoremethod)
            scores.append(abs(np.mean(score)))
    df_crossvalscore = pd.DataFrame(scores, columns = ['average score'])
    return df_crossvalscore
"""


def pca_into_columns(train_x_df, test_x_df, n_components, normalize=True):
    assert np.all(train_x_df.columns == test_x_df.columns)
    pca = PCA(n_components=n_components)
    if normalize:
        train_x_df = (train_x_df - train_x_df.mean()) / train_x_df.std()
        test_x_df = (test_x_df - test_x_df.mean()) / test_x_df.std()
    pca.fit(train_x_df)

    train_df_dict = col.OrderedDict()
    test_df_dict = col.OrderedDict()
    for component in range(n_components):
        train_df_dict[f"comp_{component}"] = (
        pd.Series(pca.components_[component, :],
                  index=train_x_df.columns) * train_x_df).sum(axis=1)
        test_df_dict[f"comp_{component}"] = (
        pd.Series(pca.components_[component, :],
                  index=test_x_df.columns) * test_x_df).sum(axis=1)
    return pd.DataFrame(train_df_dict), pd.DataFrame(test_df_dict), pca


def normalize(x, y, y_label, num_months=9, clip=None):
    column_dict = col.OrderedDict()
    for column in x.columns:
        base_column = column[:-2]
        if base_column not in column_dict:
            column_dict[base_column] = []
        column_dict[base_column].append(column)
    x_dict = col.OrderedDict()
    new_y = None
    for base_column, column_ls in column_dict.items():
        assert len(column_ls) == num_months
        columns_a = [_ for _ in column_ls if int(_.split("_")[-1]) <= 3]
        assert len(columns_a) == 3

        columns_b = [_ for _ in column_ls if int(_.split("_")[-1]) > 3]
        assert len(columns_b) == 6

        denominator = x[columns_a].sum(axis=1).replace(0, 1)
        for column in columns_b:
            x_dict[column] = x[column] / denominator
        if base_column == y_label:
            new_y = y / denominator
    new_x = pd.DataFrame(x_dict)
    assert new_y is not None

    if clip:
        clipped_new_x = new_x.clip(*clip)
        clipped_new_y = new_y.clip(*clip)
        print(
            (new_x==clipped_new_x).mean().mean(),
            (new_y==clipped_new_y).mean().mean(),
        )
        new_x = clipped_new_x
        new_y = clipped_new_y
    return new_x, new_y


def aggregate_month_columns(data, num_months = 9):
    column_dict = col.OrderedDict()
    for column in data.columns:
        base_column = column[:-2]
        if base_column not in column_dict:
            column_dict[base_column] = []
        column_dict[base_column].append(column)
    df_dict = col.OrderedDict()
    for base_column, column_ls in column_dict.items():
        assert len(column_ls) == num_months
        df_dict[base_column] = data[column_ls].sum(axis=1)
    new_df = pd.DataFrame(df_dict)
    return new_df
