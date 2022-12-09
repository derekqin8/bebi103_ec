import pandas as pd

import bokeh.io
import bokeh.plotting
import bokeh.models
import bokeh.layouts

from utils import *

bokeh.io.output_file('../interactives/interactive_all_mle.html')

data_path = 'https://s3.amazonaws.com/bebi103.caltech.edu/data/gardner_mt_catastrophe_only_tubulin.csv'

df = pd.read_csv(data_path, comment='#')

df = df.melt()
df.columns = ['tubulin concentration (uM)', 'time to catastrophe (s)']
df['tubulin concentration (uM)'] = df['tubulin concentration (uM)'].str.split(
    ' ').str.get(0).astype(int)
df = df.dropna()
df = df.sort_values('tubulin concentration (uM)')

x = df[df['tubulin concentration (uM)'] ==
       12]['time to catastrophe (s)'].values

alpha, beta = mle_log_gamma(x)
beta1, beta2 = mle_log_exp2(x)

p1 = bokeh.plotting.figure(
    frame_height=300,
    frame_width=400,
    title='MLE predictions for alpha based on a Gamma generative model',
    x_axis_label='tubulin concentration (uM)',
    y_axis_label='MLE alpha prediction'
)

p2 = bokeh.plotting.figure(
    frame_height=300,
    frame_width=400,
    title='MLE predictions for beta based on a Gamma generative model',
    x_axis_label='tubulin concentration (uM)',
    y_axis_label='MLE beta prediction'
)

p3 = bokeh.plotting.figure(
    frame_height=300,
    frame_width=400,
    title='MLE predictions for mean time to catastrophe based on a Gamma generative model',
    x_axis_label='tubulin concentration (uM)',
    y_axis_label='MLE mean prediction'
)

for conc in df['tubulin concentration (uM)'].unique():
    x = df[df['tubulin concentration (uM)'] ==
           conc]['time to catastrophe (s)'].values

    alpha, beta = mle_log_gamma(x)
    print('Tubulin Concentration (uM):', conc)
    print('MLE for alpha: '+str(alpha))
    print('MLE for beta: '+str(beta))
    print('MLE mean: '+str(alpha/beta))

    p1.circle(
        x=conc,
        y=alpha,
        color='red',
        alpha=0.5,
        size=10
    )

    p2.circle(
        x=conc,
        y=beta,
        color='blue',
        alpha=0.5,
        size=10
    )

    p3.circle(
        x=conc,
        y=alpha/beta,
        color='orange',
        alpha=0.5,
        size=10,
    )

bokeh.io.save(bokeh.layouts.column(p1, p2, p3))
