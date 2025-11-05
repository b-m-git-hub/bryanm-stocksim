from dash import Dash, dcc, html, Input, Output, State, callback, ctx
import plotly.graph_objects as go
from src import graphing
from src.portfolio import Portfolio
import pandas as pd

# Initialize the app
app = Dash()
server = app.server

# Construct an empty graph
fig = go.Figure()
# App layout
app.layout = html.Div([
    dcc.Graph(id="candlestick-graph", figure=fig),
    
    dcc.Store(id="current-price"),
    dcc.Store(id="portfolio-store", data={"cash": 1000000, "holdings": 0, "trades": []}),
    dcc.Store(id="current-timestamp"),

    html.Div([
        
        # Left Column Trading
        html.Div([
            html.Label("Update Speed (ms):"),
            dcc.Input(id="update-speed", type="number", value=1000, min=100, step=100),
            html.Button("Start/Update", id="start-button", n_clicks=0),
            dcc.Interval(id="interval-part", interval=1000, n_intervals=0, disabled=True),

            html.Div(id="current-price-display"),
            html.Div([
                html.Label("Quantity:"),
                dcc.Input(id="trade-quantity", type="number", value=1, min=1, step=1),
                html.Div([
                    html.Button("Buy", id="buy-button", n_clicks=0),
                    html.Button("Sell", id="sell-button", n_clicks=0),
                ], id="button-row")
            ], id="trade-panel"),
            html.Div(id="trade-status"),
        ], className="control-column"),
        
        # Middle Column Graph
        html.Div([
            dcc.Graph(id="small-graph", figure=go.Figure(), className="small-graph")
        ], className="graph-column"),
                    
        # Right Column Portfolio
        html.Div(id="portfolio-summary", className="summary-column")
    ], className="bottom-panel")
])


# Callback to start the graphing process
@app.callback(
    Output("interval-part", "disabled"),
    Output("interval-part", "interval"),
    Input("start-button", "n_clicks"),
    State("update-speed", "value"),
    prevent_initial_call = True
)
def activateInterval(n_clicks, speed):
    return False, speed or 1000

# Callback to update the graph
@app.callback(
    Output("candlestick-graph", "figure"),
    Output("small-graph", "figure"),
    Output("current-price", "data"),
    Output("portfolio-summary", "children"),
    Output("current-price-display", "children"),
    Output("current-timestamp", "data"),
    Input("interval-part", "n_intervals"),
    State("portfolio-store", "data"),
    prevent_initial_call = True
)
def updateGraph(n_intervals, portfolioData):
    fullFig, currentPrice, df = graphing.update(n_intervals, return_df=True)

    currentTimestamp = df["Timestamp"].iloc[-1]

    recentData = df[df["Timestamp"] >= df["Timestamp"].max() - pd.Timedelta(minutes=30)]
    miniFig = go.Figure(data=[go.Candlestick(
        x=recentData["Time"],
        open=recentData["Open"],
        high=recentData["High"],
        low=recentData["Low"],
        close=recentData["Close"],
        increasing_line_color = "green", decreasing_line_color = "red")
    ])
    miniFig.update_layout(
        title="Last 30 Minutes",
        xaxis_title="Time",
        yaxis_title="Price",
        xaxis_rangeslider_visible = False,
        showlegend = False,
        uirevision = True,
        height=450,
        margin=dict(t=30, b=30, l=40, r=40)
    )

    portfolio = Portfolio()
    portfolio.cash = portfolioData.get("cash", 1000000)
    portfolio.holdings = portfolioData.get("holdings", 0)
    portfolio.trades = portfolioData.get("trades", [])
    summary = portfolio.getPortfolio(currentPrice)

    summaryPanel = html.Div([
        html.H4("Live Portfolio Summary"),
        html.P(f"Current Cash: {summary['Cash']:.2f}"),
        html.P(f"Quantity Held: {summary['Quantity']}"),
        html.P(f"Average Cost: ${summary['Average Cost']:.2f}"),
        html.P(f"Current Price: ${summary['Current Price']:.2f}"),
        html.P(f"Unrealized ROI: {summary['Unrealized ROI']:.2f}%"),
        html.P(f"Realized ROI: {summary['Realized ROI']:.2f}%"),
        html.P(f"Profit: ${summary['Profit']:.2f}")
    ])

    for trade in portfolio.trades:
        time=trade["Time"]
        price=trade["Price"]
        action=trade["Action"]
        quantity=trade["Quantity"]

        fullFig.add_trace(go.Scatter(
            x=[time],
            y=[price],
            mode="markers",
            marker=dict(
                color="green" if action == "Buy" else "red",
                size=min(15 + quantity*1.25, 100),
                symbol="triangle-up" if action == "Buy" else "triangle-down",
                opacity=0.5,
            ),
            name=action,
            hovertext=f"{action} {quantity} @ ${price:.2f}",
            showlegend=False
        ))

    return fullFig, miniFig, currentPrice, summaryPanel, html.Div(f"Current Price: ${currentPrice:.2f}"), currentTimestamp


# Callback for buy and sell
@app.callback(
    Output("trade-status", "children"),
    Output("portfolio-store", "data"),
    Input("buy-button", "n_clicks"),
    Input("sell-button", "n_clicks"),
    State("current-price", "data"),
    State("portfolio-store", "data"),
    State("trade-quantity", "value"),
    State("current-timestamp", "data")
)
def executeTrade(buyClicks, sellClicks, currentPrice, portfolioData, quantity, timestamp):
    if currentPrice is None:
        return "No price found", portfolioData
    
    portfolio = Portfolio()
    portfolio.cash = portfolioData.get("cash", 1000000)
    portfolio.holdings = portfolioData.get("holdings", 0)
    portfolio.trades = portfolioData.get("trades", [])

    triggeredID = ctx.triggered_id
    if triggeredID == "buy-button":
        action = portfolio.buy(currentPrice, quantity, timestamp)
    elif triggeredID == "sell-button":
        action = portfolio.sell(currentPrice, quantity, timestamp)
    
    updatedPort = {
        "cash": portfolio.cash,
        "holdings": portfolio.holdings,
        "trades": portfolio.trades
    }

    return f"{action}", updatedPort

# Boilerplate
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
