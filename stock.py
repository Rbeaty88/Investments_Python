import urllib2
import time
import matplotlib.dates as mdates
import numpy as np
import mpl_finance

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pandas_datareader import data, wb, DataReader
import pandas as pd
import datetime

class StockTracker:

    def __init__(self, stock):
        currentDate = datetime.datetime.now()
        lastYear = currentDate.year - 1
        lastYearMonth = currentDate.month
        lastYearDay = currentDate.day
        self.stock_data = self.pull_data(stock, datetime.datetime(lastYear, lastYearMonth, lastYearDay), currentDate)
        

    def pull_data(self, stock, startDate, endDate):
        # Pull data for todays date and all of last year as well
        # High, Low, Open, Close, Volume, Adj Close
        
        df_stockticker = DataReader(stock, 'yahoo', startDate, endDate)
        
        #return ibm['Close']
        return df_stockticker
    
    def graphMoveAvg(self, MA1, MA2):
        # Creating moving average with pandas - MA1 should be short moving average, MA2 should be long moving average
        short_rolling = self.stock_data['Close'].rolling(window=MA1).mean()
        long_rolling = self.stock_data['Close'].rolling(window=MA2).mean()

        start_date = '2015-01-01'
        end_date = '2016-12-31'

        fig, ax = plt.subplots(figsize=(16,9))

        ax.plot(self.stock_data['Close'].loc[start_date:end_date, :].index, self.stock_data['Close'].loc[start_date:end_date, 'MSFT'], label='Price')
        #ax.plot(long_rolling.loc[start_date:end_date, :].index, long_rolling.loc[start_date:end_date, 'MSFT'], label = '100-days SMA')
        #ax.plot(short_rolling.loc[start_date:end_date, :].index, short_rolling.loc[start_date:end_date, 'MSFT'], label = '20-days SMA')

        ax.legend(loc='best')
        ax.set_ylabel('Price in $')
        ax.xaxis.set_major_formatter(my_year_month_fmt)

    def graphMovingAverage(self, MA1, MA2):
        
        Av1 = self.movingaverage(self.stock_data['Close'], MA1)
        Av2 = self.movingaverage(self.stock_data['Close'], MA2)
        
        date = self.stock_data.reset_index()['Date']
        SP = len(date[MA2-1:])
            
        fig = plt.figure(facecolor='#07000d')

        ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4, axisbg='#07000d')

        Label1 = str(MA1)+' SMA'
        Label2 = str(MA2)+' SMA'

        ax1.plot(date[-SP:],Av1[-SP:],'#e1edf9', label=Label1, linewidth=1.5)
        ax1.plot(date[-SP:],Av2[-SP:],'#4ee6fd', label= Label2, linewidth=1.5)

        ax1.grid(True, color='w')
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.yaxis.label.set_color("w")
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.tick_params(axis='y', colors='w')
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock price and Volume')
        

        plt.show()

    def movingaverage(self, values, window):
        weigths = np.repeat(1.0, window)/window
        smas = np.convolve(values, weigths, 'valid')
        return smas # as a numpy array

    def testFunction(self):
        return self.stock_data#.rolling(window=20).mean()

if __name__ == "__main__":
        print StockTracker('TSLA').graphMovingAverage(2, 3)

#print StockTracker('TSLA')
#

#print StockTracker('TSLA').graphMoveAvg(20,100)
