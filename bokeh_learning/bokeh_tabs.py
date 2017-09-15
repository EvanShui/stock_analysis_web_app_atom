from bokeh.layouts import layout, column
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, OpenURL, TapTool, CustomJS, ColumnDataSource, Tool, Div, Button


fig1 = figure()
fig1.circle([0,1,2],[1,3,2])
fig2 = figure()
fig2.circle([0,0,2],[4,-1,1])
fig3 = figure()
fig3.circle([0,4,3],[1,2,0])

fig1.js_on_event('tap', CustomJS(code="console.log('hello')"))

div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
are <i>200</i> and <i>100</i> respectively.""", width=500, height=500)

l1 = layout([[fig1, div]], sizing_mode='fixed')
l2 = layout([[fig3]],sizing_mode='fixed')

tab1 = Panel(child=l1,title="This is Tab 1")
tab2 = Panel(child=l2,title="This is Tab 2")
tabs = Tabs(tabs=[ tab1, tab2 ])

curdoc().add_root(column(tabs))
