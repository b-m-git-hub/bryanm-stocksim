# S&P500 Historical Data Trading Simulator
Interactive Dash/Plotly app using historical intraday S&P500 stock data to create a candlestick chart with trade logging and portfolio analytics.

**Check it out on Heroku: link**

**Fun fact:** The data is taken in one minute intervals allowing for more accurate trades, but don't worry you can set how fast (or slow) you want the data to appear.

## How to Run Locally:

```bash
git clone https://github.com/b-m-git-hub/bryanm-stocksim.git
pip install -r requirements.txt
python app.py
```

## How It's Made:

**Tech used:** Python, Dash, Plotly, pandas, CSS

The first step was to scrape the data using the Yahoo Finance library in Python. Since the data in 1 minute intervals is only available for free for 30 days on Yahoo Finance, I had to pick just one stock as I would need to get the data myself day by day. I decided on the S&P500 as it would best encompass the market as a whole and it isn't too outrageously priced for the purposes of a mock portfolio. I used the Yahoo Finance library in Python for this and saved it as a csv in a data folder.

Then it was on to processing the data and turning it into something usable. For this I used pandas to create a dataframe. I then had to remove the date from the time data column as knowing the exact date the data is from would undermine the project's purpose.

With the data cleaned up and prepared, it was time to display the data. I chose to use Dash with Plotly to create an interactive graph. I decided on a candlestick graph as it is the gold standard for viewing stocks due to the large range of information they provide. A basic graphing file and Dash setup were created to ensure the graph looked as intended. Both were modified to ensure the graph updated with one piece of data at a time. As the graph gets larger, it is very difficult to see the actual candlesticks. As a result, there is a smaller graph that only shows the past 30 minutes to allow for a view of the big picture as well as the most recent data.

Once the graph was updating and working properly, it was time to implement trading and a portfolio to track the trades. Buys and sells are calculated based on the close price of the current candlestick and can be of any quantity as long as you have the money or number of stocks. The portfolio starts at $1,000,000 to allow for a large quantity of stocks to be bought.

## Lessons Learned:

Expectations are not reality! Going into this project I had about a million ideas. Once I started getting deeper into it, I realized many of those ideas will not be able to come to fruition or at least not to the capacity I envisioned.
I learned a great deal about how important the organization of your code is as well as the actual folders of your project. Even with this in mind, my project could be organized much better, but now I know for the future to always have it in the back of my mind.