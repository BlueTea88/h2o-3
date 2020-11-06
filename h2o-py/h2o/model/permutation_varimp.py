# -*- encoding: utf-8 -*-
"""
H2O Permutation Feature Importance.

:copyright: (c) 2020 H2O.ai
:license:   Apache License Version 2.0 (see LICENSE for details)
"""

import h2o
from h2o.frame import H2OFrame
from h2o.expr import ExprNode
from h2o.model.model_base import _get_matplotlib_pyplot
from h2o.utils.shared_utils import can_use_pandas


def permutation_varimp(model, frame, use_pandas=True, metric="mse"):
    """
    Get Permutation Variable Importance Frame. 
    :param model: model after training
    :param frame: training frame
    :param use_pandas: select true to return pandas data frame
    :param metric: (str) loss function metrics to be used 
    :return: H2OFrame or Pandas data frame
    """
    
    if type(frame) is not H2OFrame:
        raise ValueError("Frame is not H2OFrame")

    m_frame = H2OFrame._expr(ExprNode("PermutationVarImp", model, frame, metric))

    if use_pandas and can_use_pandas():
        import pandas
        pd = h2o.as_list(m_frame)
        return pandas.DataFrame(pd, columns=pd.columns)
    
    return m_frame


def plot_permutation_var_imp(importance, algo_name, metric="mse", server=False):
    """
    Plot Permutation Variable Importance, by default scaled importance is plotted
    Inspired from model_base.varimp_plot() to stay consistent with the manner of plotting
    :param importance: frame of variable importance
    :param algo_name: algorithm of the model
    :param metric: loss function metric that was used for calculation
    :param Specify whether to activate matplotlib "server" mode. In this case, the plots are saved to a file instead of being rendered.
    :return: 
    """
    
    importance_val = []
    for col in importance.columns:
        if col == "importance":
            continue    # has string values
        importance_val.append(importance.loc[2][col])

    # specify bar centers on the y axis, but flip the order so largest bar appears at top
    pos = range(len(importance_val))[::-1]

    num_of_features = min(len(importance_val), 10)
    plt = _get_matplotlib_pyplot(server)
    if not plt: return

    fig, ax = plt.subplots(1, 1, figsize=(14, 10))

    plt.barh(pos[0:num_of_features], importance_val[0:num_of_features], align="center",
             height=0.8, color="#1F77B4", edgecolor="none")
    # Hide the right and top spines, color others grey
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_color("#7B7B7B")
    ax.spines["left"].set_color("#7B7B7B")
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position("left")
    ax.xaxis.set_ticks_position("bottom")
    plt.yticks(pos[0:num_of_features], importance.columns[1:num_of_features + 1])   # col 0 is str: importance
    plt.ylim([min(pos[0:num_of_features]) - 1, max(pos[0:num_of_features]) + 1])
    # ax.margins(y=0.5)
    plt.title("Permutation Variable Importance: " + algo_name + " (" + metric + ")", fontsize=20)
    if not server:
        plt.show()