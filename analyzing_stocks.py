import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# make function for dashboard
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=True,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    

#### Extract stock data with yfinance API
## Extract Tesla stock data
# create ticker object. ticker symbol for tesla is TSLA
tsla = yf.Ticker("TSLA")
# get data for max period
tesla_data = tsla.history(period = "max")
# reset index 
tesla_data.reset_index(inplace = True)
print(tesla_data.head(5))


## Extract Gamestop stock data
 # create ticker object. ticker symbol for Gamestop is GME
gme = yf.Ticker("GME")
# get data for max period
gme_data = gme.history(period = "max")
# reset index 
gme_data.reset_index(inplace = True)
print(gme_data.head(5))



#### Use Webscraping to extract Company revenue
## Extract company revenue for tesla
# get htlm text data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
# Parse html with beuatifulsoup
soup = BeautifulSoup(html_data, "html.parser")
# Exctract table data.
tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"]) # create empty dataframe with Date and Revenue columns
for row in soup.find_all("tbody")[1].find_all("tr"): #needed table is second table in html. index1. tr is html for table row
    cells = row.find_all("td") # td is html for table data cell elements
    date = cells[0].text
    revenue = cells[1].text
    tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)# append info to dataframe

### Alternative ways to extract table info from url
## Directly from url
# # tesla_revenue2 = pd.read_html(url)[1]
# # tesla_revenue2.columns = ["Date", "Revenue"]

## From beautiful soup object
# tesla_revenue3 = pd.read_html(str(soup))[1]
# tesla_revenue3.columns = ["Date", "Revenue"]

# Remove "," and "$" in Revenue column
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
# Remove missing values. Removing na and filter to remove empty values
tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""] 
print(tesla_revenue.head(5))



### Extract company revenue for Gamestop
# get htlm text data
url2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data2 = requests.get(url2).text
# Parse html with beuatifulsoup
soup2 = BeautifulSoup(html_data2, "html.parser")
# Exctract table data.
gme_revenue = pd.DataFrame(columns = ["Date", "Revenue"])
for row in soup2.find_all("tbody")[1].find_all("tr"):
    cells = row.find_all("td")
    date = cells[0].text
    revenue = cells[1].text
    gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)
    
# remove , and dollar sign
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",|\$","")

# drop na's and filter for values that are not empty
gme_revenue.dropna(inplace = True)

gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]
print(tesla_revenue.head(5))



### Create Dashboards
# For Tesla
make_graph(tesla_data, tesla_revenue, 'Tesla')

# For Gamestop
make_graph(gme_data, gme_revenue, 'GameStop')

