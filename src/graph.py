import sys
import pandas as pd
import mplfinance as mpf
import data_processing
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class CandlestickChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S&P500 Candlestick Charts")
        self.setGeometry(500, 500, 2500, 1500)
        
        self.randomDataset = data_processing.random_data("data/")
        self.data = data_processing.load_data(self.randomDataset)
        self.data.loc[:, "Datetime"] = pd.to_datetime(self.data["Datetime"], errors = "coerce")

        self.fig = Figure(figsize = (6,5))
        grid = self.fig.add_gridspec(2, 1, height_ratios = [3, 1])
        self.canvas = FigureCanvas(self.fig)
        self.ax1 = self.fig.add_subplot(grid[0]) # 30 minute chart
        self.ax2 = self.fig.add_subplot(grid[1], sharex = self.ax1) # Full chart

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setStretchFactor(self.canvas, 2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

        self.update_graph()

    def update_graph(self):
        
        nextData = self.data.iloc[1]
        if nextData.empty:
            return
        self.data = pd.concat([self.data, nextData], ignore_index = True)
        if "Datetime" not in self.data.columns:
            print("Datetime not found")
            return
        self.data.set_index("Datetime", inplace = True)
        
        self.ax1.clear()
        self.ax2.clear()

        # Keyword arguments and custom style for plotting
        mc = mpf.make_marketcolors(up = "g", down = "r")
        s = mpf.make_mpf_style(marketcolors = mc)
        mpf.plot(self.data, type = "candle", mav = (8,21,55), volume = self.ax2, style = s, ax = self.ax1)
        
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CandlestickChart()
    window.show()
    sys.exit(app.exec_())
