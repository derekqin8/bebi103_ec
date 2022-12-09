# %%
import pandas as pd

import bokeh.io
import bokeh.plotting
import bokeh.models
import bebi103

from utils import *

bokeh.io.output_file('../interactives/interactive_ecdf.html')

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

gamma_samples = sample_gamma(alpha, beta, len(x))
exp2_samples = sample_exp2(beta1, beta2, len(x))

ecdf_tabs = []

ecdf_gamma = bebi103.viz.predictive_ecdf(
    samples=gamma_samples, data=x, x_axis_label="n"
)

ecdf_tabs.append(bokeh.models.widgets.Panel(
    child=ecdf_gamma,
    title='Gamma Model'
))

ecdf_exp2 = bebi103.viz.predictive_ecdf(
    samples=exp2_samples, data=x, x_axis_label="n"
)

ecdf_tabs.append(bokeh.models.widgets.Panel(
    child=ecdf_exp2,
    title='2 Poisson Process Model'
))

bokeh.io.save(bokeh.models.widgets.Tabs(tabs=ecdf_tabs))
# %%
