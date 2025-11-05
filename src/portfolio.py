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
        realizedCost = 0

        for trade in self.trades:
            action = trade["Action"]
            price = trade["Price"]
            qty = trade["Quantity"]

            if action == "Buy":
                buyStack.append([price, qty])

            elif action == "Sell":
                sellQty = qty
                sellPrice = price

                while sellQty > 0 and buyStack:
                    buyPrice, buyQty = buyStack[0]
                    matchedQty = min(buyQty, sellQty)

                    realizedProfit += (sellPrice - buyPrice) * matchedQty
                    realizedCost += buyPrice * matchedQty

                    sellQty -= matchedQty
                    buyQty -= matchedQty

                    if buyQty == 0:
                        buyStack.pop(0)
                    else:
                        buyStack[0][1] = buyQty

        unrealizedCost = sum(price * qty for price, qty in buyStack)
        unrealizedValue = self.holdings * currentPrice
        unrealizedProfit = unrealizedValue - unrealizedCost

        realizedROI = (realizedProfit / realizedCost) * 100 if realizedCost else 0
        unrealizedROI = (unrealizedProfit / unrealizedCost) * 100 if unrealizedCost else 0

        totalValue = self.cash + (self.holdings * currentPrice)
        profit = totalValue - INITIAL_CASH

        return {
            "Realized ROI": realizedROI,
            "Unrealized ROI": unrealizedROI,
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
        
        roi = self.calculateRoi(currentPrice)

        return {
            "Cash": self.cash,
            "Quantity": self.holdings,
            "Average Cost": aveCost,
            "Current Price": currentPrice,
            "Unrealized ROI": roi["Unrealized ROI"],
            "Realized ROI": roi["Realized ROI"],
            "Profit": roi["Profit"]
        }