import datetime as dt
import itertools


def split_field_month(s):
    return s.rsplit("_", 1)


def map_to_month(s):
    year, month = map(int, split_field_month(s)[1].split("-"))
    return dt.datetime(year, month, 1)


def map_to_monthint(s):
    name, monthint = s.rsplit("_", 1)
    return name, int(monthint)


def flatten_list(ls):
    return list(itertools.chain(*ls))


def select_col(df, lam):
    return [column for column in df.columns if lam(column)]


def dictmap(func, ls):
    return dict(zip(ls, map(func, ls)))


def indexmap(df_or_srs, func):
    df_or_srs = df_or_srs.copy()
    df_or_srs.index = map(func, df_or_srs.index)
    return df_or_srs


def columnmap(df, func):
    df = df.copy()
    df.columns = map(func, df.columns)
    return df

