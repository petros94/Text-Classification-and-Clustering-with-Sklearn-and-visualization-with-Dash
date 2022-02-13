import numpy as np
from plotly import tools
import plotly.graph_objects as go


def plot_decision_boundary(clf, X, labels):
    y = labels
    h = .02  # step size in the mesh

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h)
                         , np.arange(y_min, y_max, h))
    y_ = np.arange(y_min, y_max, h)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    fig = tools.make_subplots(rows=1, cols=1,
                              subplot_titles=("Decision boundary")
                              )

    trace1 = go.Heatmap(x=xx[0], y=y_, z=Z,
                        showscale=False)

    trace2 = go.Scatter(x=X[:, 0], y=X[:, 1],
                        mode='markers',
                        showlegend=False,
                        marker=dict(size=10,
                                    color=y,
                                    line=dict(color='black', width=1))
                        )

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)


    for i in map(str, range(1, 2)):
        x = 'xaxis' + i
        y = 'yaxis' + i
        fig['layout'][x].update(showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                ticks='',
                                autorange=True)
        fig['layout'][y].update(showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                ticks='',
                                autorange=True)

    return fig