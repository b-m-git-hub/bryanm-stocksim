import pandas as pd

INITIAL_CASH = 1000000


class Portfolio:

    def __init__(self):
        self.cash = INITIAL_CASH
        self.holdings = 0
        self.trades = []
    
    def buy(self, price, quantity=1, timestamp=None):
        timestampStr = pd.to_datetime(timestamp).strftime("%H:%M:%S")
        totalCost = price * quantity
        if self.cash >= totalCost:
            self.holdings += quantity
            self.cash -= totalCost
            self.trades.append({"Action": "Buy", "Price": price, "Quantity": quantity, "Time": timestampStr})
            return f"Bought {quantity} at ${price:.2f}"
        return "Insufficient funds."
    
    def sell(self, price, quantity=1, timestamp=None):
        timestampStr = pd.to_datetime(timestamp).strftime("%H:%M:%S")
        if self.holdings >= quantity:
            self.holdings -= quantity
            self.cash += price * quantity
            self.trades.append({"Action": "Sell", "Price": price, "Quantity": quantity, "Time": timestampStr})
            return f"Sold {quantity} at ${price:.2f}"
        return "Not enough stock to sell."
    
    def calculateRoi(self, currentPrice):
        buyStack = []
        realizedProfit = 0

        for trade in self.trades:
            price = trade["Price"]
            if trade["Action"] == "Buy":
                buyStack.append(price)
            elif trade["Action"] == "Sell" and buyStack:
                buyPrice = buyStack.pop(0)
                realizedProfit += price - buyPrice

        unrealizedCost = sum(buyStack)
        unrealizedValue = self.holdings * currentPrice
        unrealizedProfit = unrealizedValue - unrealizedCost

        principal = sum(trade["Price"] for trade in self.trades if trade["Action"] == "Buy")
        profit = INITIAL_CASH - self.cash

        return {
            "Realized ROI": f"{(realizedProfit / principal) * 100:.2f}%" if principal else "0.00%",
            "Unrealized ROI": f"{(unrealizedProfit / principal) * 100:.2f}%" if principal else "0.00%",
            "Profit": profit
        }

    def getPortfolio(self, currentPrice):
        totalCost = 0
        totalQuantity = 0

        for trade in self.trades:
            if trade["Action"] == "Buy":
                totalCost += trade["Price"]
                totalQuantity += 1
        
        aveCost = totalCost / totalQuantity if totalQuantity else 0
        unrealizedProfit = (currentPrice - aveCost) * self.holdings
        unrealizedRoi = (unrealizedProfit / (aveCost * self.holdings)) * 100 if self.holdings else 0
        
        roi = self.calculateRoi(currentPrice)

        return {
            "Cash": self.cash,
            "Quantity": self.holdings,
            "Average Cost": aveCost,
            "Current Price": currentPrice,
            "Unrealized ROI": unrealizedRoi,
            "Realized ROI": roi["Realized ROI"],
            "Profit": roi["Profit"]
        }