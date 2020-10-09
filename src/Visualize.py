import os 
import pandas as pd
from matplotlib import pyplot as plt

class Visualize:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.visualise()
    
    def visualise(self):
        data = pd.io.parsers.read_csv(os.path.join(self.data_dir, "equity.csv"), header=0, parse_dates=True, index_col=0)
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)
        fig.patch.set_facecolor("white")
        
        # plot equity curve
        # =================
        ax1.set_ylabel("Portfolio Value, %")
        data["equity_curve"].plot(ax=ax1, color="blue", lw=2)
        ax1.grid(True)

        # plot return
        # ===========
        ax2.set_ylabel("Period returns, %")
        data["returns"].plot(ax=ax2, color="black", lw=2)
        ax2.grid(True)

        # plot drawdown
        # =============
        ax3.set_ylabel("Drawdowns, %")
        data["drawdown"].plot(ax=ax3, color="red", lw=2)
        ax3.grid(True)

        plt.subplots_adjust(hspace=0.3)
        plt.show()