import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3 #@UnresolvedImport
from bokeh.models.tools import HoverTool


output_file('types_of_munitions.html')

df = pd.read_csv('thor_wwii.csv')

filter = df['COUNTRY_FLYING_MISSION'].isin(('USA','GREAT BRITAIN'))
df = df[filter]

grouped = df.groupby('COUNTRY_FLYING_MISSION')['TONS_IC', 'TONS_FRAG', 'TONS_HE'].sum()


#convert tons to kilotons again
grouped = grouped / 1000

source = ColumnDataSource(grouped)
countries = source.data['COUNTRY_FLYING_MISSION'].tolist()
p = figure(x_range=countries)

p.vbar_stack(stackers=['TONS_FRAG', 'TONS_HE', 'TONS_IC'],
             x='COUNTRY_FLYING_MISSION', source=source,
             legend = ['High Explosive', 'Fragmentation', 'Incendiary'],
             width=0.5, color=Spectral3)

################## MADE BY ME ##################
hover = HoverTool()
hover.tooltips = [
    ('Number of High Explosive', '@TONS_HE'),
    ('Number of Fragmentation', '@TONS_FRAG'),
    ('Number of Incendiary', '@TONS_IC')
]
p.add_tools(hover)
#################################################

p.title.text ='Types of Munitions Dropped by Allied Country'
p.legend.location = 'top_left'

p.xaxis.axis_label = 'Country'
p.xgrid.grid_line_color = None	#remove the x grid lines

p.yaxis.axis_label = 'Kilotons of Munitions'

show(p)

