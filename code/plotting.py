import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import data
import utils

import matplotlib.cm as cm


def repeat_palette(palette, times):
    ls = []
    for color in palette:
        for time in range(times):
            ls.append(color)
    return "".join(ls)


def get_colors(n):
    return cm.rainbow(np.linspace(0, 1, n))


def repeated_colors(n, times):
    return repeat_palette(get_colors(n), times)


# Select top 30 coefficients for plotting
def select_top30_coef(coefficients_input, selected_columnnames):
    order = list(np.argsort(coefficients_input))
    colname_top30coef = [selected_columnnames[i] for i in order[-30:]]
    top30coef = [coefficients_input[i] for i in order[-30:]]
    return colname_top30coef, top30coef


# Graph of coefficient/feature importance
def graphcoefficient(selected_coef, dfcolumnnames, plot_title):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(range(len(selected_coef)), selected_coef, width=0.1, color='b')
    ax.set_xticks(np.arange(len(selected_coef)))
    ax.set_xticklabels(dfcolumnnames, rotation=90)
    plt.title(plot_title)
    ax.set_ylabel('coef')


def plot_normalized_distribution_over_time(raw_data_df):
    fig, axes = plt.subplots(4, 3, figsize=(16, 16))
    flat_axes = utils.flatten_list(axes)
    for i, (field_name, ax) in enumerate(zip(data.FIELD_NAMES, flat_axes)):
        x1 = raw_data_df[[
            _ for _ in raw_data_df.columns
            if utils.split_field_month(_)[0] == field_name
            ]]
        x2 = x1.div(x1.sum(axis=1), axis=0)
        x3 = x2.mean()
        x3.index = pd.DatetimeIndex(x3.index.map(utils.map_to_month)) \
            .strftime("%Y-%m")
        x3.plot(kind="bar", ax=ax, color="ggg"+"b"*(len(x3)-3))
        ax.set_title(data.FIELD_NAMES_MAP[field_name], fontsize=18)
        ax.set_xticks([])

    # Hack
    for ax in flat_axes[-3:]:
        ax.set_xticks(range(len(x3.index)))
        ax.set_xticklabels([
                               _ if i % 3 == 0 else ""
                               for (i, _) in enumerate(x3.index)
                               ])
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=60)

    fig.suptitle("Normalized Distribution of Activity over Time",
                 fontsize=30)


def format_field_monthint_name_minus(s):
    name, monthint = utils.map_to_monthint(s)
    offset = monthint - 13
    return f"{name} (M={offset})"


def format_field_monthint_name_minus2(s):
    name, monthint = utils.map_to_monthint(s)
    offset = monthint - 13
    return f"{data.FIELD_NAMES_MAP[name]} (M={offset})"
