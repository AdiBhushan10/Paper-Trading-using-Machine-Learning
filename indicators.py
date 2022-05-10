""""""
"""Project 8: INDICATORS 		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  	  			  		 			     			  	 
All Rights Reserved  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  	  			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  	  			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  	  			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  			  		 			     			  	 
or edited.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  	  			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  	  			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  			  		 			     			  	 
GT honor code violation.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  	  			  		 			     			  	 
GT User ID: abhushan30 (replace with your User ID)  		  	   		  	  			  		 			     			  	 
GT ID: 903630361 (replace with your GT ID)  		  	   		  	  			  		 			     			  	 
"""

import datetime as dt
import os

import numpy as np
import matplotlib.pyplot as myPlot
import pandas as pd
from util import get_data, plot_data

def author():
    return "abhushan30"

def myIndicators(normFr,symbol='JPM',sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31), lookback=50):
    '''
    myFrame = get_data([symbol], pd.date_range(sd,ed), True, colname='Adj Close').drop(columns=['SPY'])
    myFrame = myFrame.fillna(method='ffill').fillna(method='bfill')
    normFr = myFrame/myFrame.iloc[0]
    #print(normFr)
    '''
    # 1. SMA
    simplema = normFr.rolling(window=lookback).mean()
    smaPrice = normFr/simplema
    '''
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(simplema, label="SMA", color='purple')
    myPlot.plot(smaPrice, label="Price/SMA",color='green')
    myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Normalized Prices')
    myPlot.legend()
    myPlot.title('Simple Moving Average (SMA) w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('SSMA_ind.png')
    myPlot.close()
    '''

    # 2. Momentum
    motm = normFr.pct_change(lookback)
    #motm1 = myFrame/myFrame.shift(lookback) - 1
    '''
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(motm, label="Momentum (Rolling 50-Day)", color='purple')
    #myPlot.plot(motm1, label="Momentum1 (Rolling 50-Day)", color='green')
    #myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Momentum')
    myPlot.legend()
    myPlot.title('Momentum w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('Momentum_ind.png')
    myPlot.close()
    '''
    # 3. Volatility
    voly = normFr.rolling(window=lookback).std()
    '''
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(voly, label="Volatility (Rolling 50-Day)", color='purple')
    myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Volatility')
    myPlot.legend()
    myPlot.title('Volatility w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('Volatility_ind.png')
    myPlot.close()
    '''


    # 4. EMA
    expoma = normFr.ewm(span=lookback).mean()
    '''
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(simplema, label="SMA (Rolling 50-Day)", color='purple')
    myPlot.plot(expoma, label="EMA (Rolling 50-Day)", color='green')
    #myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Exponential Moving Average')
    myPlot.legend()
    myPlot.title('Exponential Moving Average w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('EMA_ind.png')
    myPlot.close()
    '''

    # 5. BBP
    upLmt = simplema + 2*voly
    lwLmt = simplema - 2*voly
    bbper = (normFr - lwLmt) / (upLmt - lwLmt)
    '''
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(simplema, label="SMA", color='purple')
    myPlot.plot(lwLmt, label="Lower", color='cyan')
    myPlot.plot(upLmt, label="Upper", color='green')
    myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Price')
    myPlot.legend()
    myPlot.title('Bollinger Bands w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('BB_ind.png')
    myPlot.close()
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(bbper, label="Bollinger Band Percentage", color='purple')
    myPlot.plot(normFr, label="Normalized Price", color='red')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Percentage')
    myPlot.legend()
    myPlot.title('Bollinger Band Percentage w.r.t Dates')
    #myPlot.show()
    myPlot.savefig('BBP_ind.png')
    myPlot.close()
    '''
    return simplema, smaPrice, motm, bbper

#if __name__ == "__main__":
#    myIndicators()
