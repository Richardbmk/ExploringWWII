import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Range1d
from bokeh.layouts import layout
from bokeh.palettes import Spectral3 #@UnresolvedImport
from bokeh.tile_providers import CARTODBPOSITRON #@UnresolvedImport
from pyproj import Proj, transform

output_file('mapping_targets.html')

#helper function to convert lat/long to easting/northing for mapping
#this relies on functions from the pyproj library
def LongLat_to_EN(long, lat):
    try:
      easting, northing = transform(
        Proj(init='epsg:4326'), Proj(init='epsg:3857'), long, lat)
      return easting, northing
    except:
      return None, None

df = pd.read_csv('thor_wwii.csv')


#helper to convert all lat/long to webmercator and stores in new column
df['E'], df['N'] = zip(*df.apply(lambda x: LongLat_to_EN(x['TGT_LONGITUDE'], x['TGT_LATITUDE']), axis=1))


grouped = df.groupby(['E', 'N'])['TONS_IC', 'TONS_FRAG'].sum().reset_index()

filter = grouped['TONS_FRAG']!=0

grouped = grouped[filter]

source = ColumnDataSource(grouped)

left = -2150000
right = 18000000
bottom = -5300000
top = 11000000

p = figure(x_range=Range1d(left, right), y_range=Range1d(bottom, top))

p.add_tile(CARTODBPOSITRON)
p.circle(x='E', y='N', source=source, line_color='grey', fill_color='yellow')

p.axis.visible = False

show(p)