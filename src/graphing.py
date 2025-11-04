import plotly.graph_objects as go
from src import data_processing

# Get the data to construct the graph
randomDataset = data_processing.randomData("data/")
df = data_processing.loadData(randomDataset)

def update(n, return_df=False):
    end = min(n, len(df))
    newData = df.iloc[:end]
    currentPrice = newData["Close"].iloc[-1]

    fig = go.Figure(data=[go.Candlestick(
        x = newData["Time"],
        open = newData["Open"],
        high = newData["High"],
        low = newData["Low"],
        close = newData["Close"],
        increasing_line_color = "green", decreasing_line_color = "red")
    ])
    fig.update_layout(
        title = "S&P500 Candlestick Chart",
        xaxis_title = "Time",
        yaxis_title = "Price",
        xaxis_rangeslider_visible = False,
        showlegend = False,
        uirevision = True
    )
    
    
    if return_df:
        return fig, currentPrice, newData
    else:
        return fig, currentPrice
