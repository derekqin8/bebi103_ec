import pandas as pd
import numpy as np
import scipy.stats
import scipy.special

import bokeh.plotting
import bokeh.io
import bebi103
from utils import *

bokeh.io.output_file('../interactives/interactive_cr.html')

data_path = 'https://s3.amazonaws.com/bebi103.caltech.edu/data/gardner_mt_catastrophe_only_tubulin.csv'

df = pd.read_csv(data_path, comment='#')

df = df.melt()
df.columns = ['tubulin concentration (uM)', 'time to catastrophe (s)']
df['tubulin concentration (uM)'] = df['tubulin concentration (uM)'].str.split(
    ' ').str.get(0).astype(int)
df = df.dropna()
df = df.sort_values('tubulin concentration (uM)')

tabs = []

alpha = 0.05
B = 10000

print('Computing confidence regions')

for conc in df['tubulin concentration (uM)'].unique():
    x = df[df['tubulin concentration (uM)'] ==
           conc]['time to catastrophe (s)'].values

    pbs_mle = gamma_pbs_mle(x, B)

    df_npbs = pd.DataFrame(data=pbs_mle, columns=["alpha*", "beta*"])

    p_corner = bebi103.viz.corner(
        samples=df_npbs,
        parameters=["alpha*", "beta*"],
        show_contours=True,
        levels=[0.95],
    )

    tabs.append(bokeh.models.widgets.Panel(
        child=p_corner,
        title='{} uM Tubulin'.format(conc)
    ))

bokeh.io.save(bokeh.models.widgets.Tabs(tabs=tabs))
