import pandas as pd

import bokeh.io
import bokeh.plotting
import bokeh.models
import bokeh.layouts
import iqplot

from utils import *

bokeh.io.output_file('../interactives/interactive_eda.html')

data_path = 'https://s3.amazonaws.com/bebi103.caltech.edu/data/gardner_mt_catastrophe_only_tubulin.csv'

df = pd.read_csv(data_path, comment='#')

df = df.melt()
df.columns = ['tubulin concentration (uM)', 'time to catastrophe (s)']
df['tubulin concentration (uM)'] = df['tubulin concentration (uM)'].str.split(
    ' ').str.get(0).astype(int)
df = df.dropna()
df = df.sort_values('tubulin concentration (uM)')

p1 = iqplot.ecdf(
    data=df,
    q='time to catastrophe (s)',
    cats='tubulin concentration (uM)',
    marker_kwargs={'size': 1},
)

p1.legend.title = 'Tubulin Concentration (uM)'

p2 = iqplot.stripbox(
    data=df,
    q='time to catastrophe (s)',
    cats='tubulin concentration (uM)',
    spread='jitter',
    marker_kwargs={'size': 1},
    top_level='box'
)

p2.yaxis.axis_label = 'Tubulin Concentration (uM)'

bokeh.io.save(bokeh.layouts.column(p1, p2))
