from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file, ColumnDataSource
import numpy as np
from bokeh.io import curdoc
from datetime import date
from dateutil.relativedelta import *
import math
from bokeh.models import Range1d

delta_7_days = date.today() + relativedelta(days=-7)
delta_month = date.today() + relativedelta(months=-1)
delta_3_months = date.today() + relativedelta(months=-3)
delta_6_months = date.today() + relativedelta(months=-6)
delta_year = date.today() + relativedelta(years=-1)
delta_5_year = date.today() + relativedelta(years=-5)
dates = [delta_7_days, delta_month, delta_3_months, delta_6_months, delta_year, delta_5_year]

# str -> lst
# Hard coded to specifically scrape the google website and returns a list of
# the website titles from the google search results given a string to initate
# the search query
def web_scraper(day, month, year):
    lst = []
    opener = urllib.request.build_opener()
    #use Mozilla because can't access chrome due to insufficient privileges
    #only use for google
    #opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    #url for search query
    url = "http://www.marketwatch.com/search?q=ATVI&m=Ticker&rpp=15&mp=2005&bd=true&bd=false&bdv=" + str(month) + "%2F" + str(day) + "%2F20" + str(year) + "&rs=true"
    page = opener.open(url)
    soup = BeautifulSoup(page, "html.parser")
    #use beauitful soup to find all divs with the r class, which essentially
    #is the same as finding all of the divs that contain each individiaul search

    soup_tuple_list = zip(soup.findAll(class_="searchresult"), soup.findAll(class_="deemphasized")[1:-1])
    #iterating through a tags which includes title and links
    #for x in soup.findAll(class_="searchresult"):
    #appends the title of each individual search result to a list
    #    lst.append(x.a.encode("utf-8"))
    #iterating through time published and publishing company
    #gets rid of the prev strings at the beginning and end of the resulting list
    for article, date in soup_tuple_list:
        time = date.contents[1][5:]
        time = re.findall(r'\|.[A-Za-z ]*', time)[0]
        info = date.contents[0].string + time
        article.a['target']="_blank"
        lst.append((article.a.encode("utf-8"),info))
    return lst

def get_data(stock_ticker):
    ts = TimeSeries(key='VVKDMK4DCJUF1NQP', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=stock_ticker, outputsize='full')
    return data,meta_data

data,meta_data = get_data("nflx")


#print(list(int(data.tail(1).values)))
print([int(x) for x in (data.tail(1).values)[0]])

def data_to_CDS(stock_ticker, data, start_date):
    delta_days = np.busday_count(start_date, date.today())
    print(delta_days)
    data['ticker'] = stock_ticker
    adjusted_data = data.tail(delta_days)
    source = ColumnDataSource(data=dict(
        date=np.array(adjusted_data['close'].index, dtype=np.datetime64),
        price=adjusted_data['close'].values,
        index=adjusted_data['ticker']
    ))
    return source

def y_min_max(data, index):
    delta_days = np.busday_count(dates[index], date.today())
    adjusted_data = data.tail(delta_days)
    maxVal = adjusted_data['close'].max()
    minVal = adjusted_data['close'].min()
    return ((minVal - 5), (maxVal + 5))

#print(data['close'].tail(7))
#print(type(data.index[0]))
source = ColumnDataSource(data)

#print(source.data['close'].index)

#print(type(source2.data['date'][0]))
#print(source2.data['price'])
source = data_to_CDS("nflx", data, delta_5_year)
f = figure(x_axis_type="datetime")
f.line('date', 'price', source=source, line_width=2)
f.x_range = Range1d(start=dates[4],end=date.today())
y_limit = (y_min_max(data, 4))
curdoc().add_root(f)
