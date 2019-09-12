import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

from bokeh.palettes import RdGy5 #@UnresolvedImport
from bokeh.transform import factor_cmap
output_file('munitions_by_country.html')

df = pd.read_csv('thor_wwii.csv')

grouped = df.groupby('COUNTRY_FLYING_MISSION')['TOTAL_TONS',
                                               'TONS_HE', 'TONS_IC', 'TONS_FRAG'].sum()
# print(grouped)

grouped = grouped / 1000

source = ColumnDataSource(grouped)
countries = source.data['COUNTRY_FLYING_MISSION'].tolist()
p = figure(x_range=countries)

color_map = factor_cmap(field_name='COUNTRY_FLYING_MISSION',
                    palette=RdGy5, factors=countries)

p.vbar(x='COUNTRY_FLYING_MISSION', top='TOTAL_TONS',
       source=source, width=0.70, color=color_map)

p.title.text = 'Munitions Droppen by Allied Country'
p.xaxis.axis_label = 'Country'
p.yaxis.axis_label = 'Kilotons of Munitions'

hover = HoverTool()
hover.tooltips = [
    ("Totals", "@TONS_HE High Explosive / @TONS_IC Incendiary / @TONS_FRAG Fragmentation")
]

hover.mode = 'vline'

p.add_tools(hover)

show(p)



