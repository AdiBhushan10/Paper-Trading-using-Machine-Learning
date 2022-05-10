""""""
"""Project 8: Market simulator.  		  	   		  	  			  		 			     			  	 
  		  	   		  	  			  		 			     			  	 
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

import pandas as pd
from util import get_data, plot_data

def author():
    return "abhushan30"

def compute_portvals(
        orders_file,  # "./orders/orders.csv",
        start_val=100000,
        commission=0.0,
        impact=0.0,
):
    """
    Computes the portfolio values.
    """
    # 1. Prepare Prices Data Frame:
    myOrders = orders_file  # pd.read_csv(orders_file,usecols=['Date','Symbol','Order','Shares'],na_values=['nan'],index_col='Date', parse_dates=True)
    # print(myOrders)
    myOrders.sort_index(inplace=True)
    myPrices = get_data(myOrders['Symbol'].unique().tolist(), pd.date_range(myOrders.index.min(), myOrders.index.max()))
    # print(myPrices)
    # get_Data add SPY which we do not want
    if 'SPY' not in myOrders['Symbol'].unique().tolist():
        myPrices.drop('SPY', axis=1, inplace=True)
    # print(myPrices)
    myPrices['Cash'] = np.ones(myPrices.shape[0])
    # case when we have incomplete data or missing values
    myPrices = myPrices.fillna(method="ffill").fillna(method="bfill")

    # 2. Prepare Trades Data Frame:
    myTrades = myPrices.copy()
    myTrades[:] = 0.0
    # myTrades.loc[myTrades.index[0], 'Cash'] = start_val
    myTrades[0, -1] = start_val
    # print(myTrades)
    for id, data in myOrders.iterrows():
        symb, ordtyp, numShar = data['Symbol'], data['Order'], data['Shares']
        sharPrice = myPrices.loc[id, symb]
        sign_trade = 1 if ordtyp == 'BUY' else -1
        myTrades.loc[id, symb] += (sign_trade * numShar)
        sharPrice += (sign_trade * impact * sharPrice)  # Transaction Costs: Impact
        myTrades.loc[id, 'Cash'] -= (commission + (sign_trade * numShar * sharPrice))  # Transaction Costs: Commission
    # print(myTrades)

    # 3. Prepare Holdings Data Frame:
    myHolds = myTrades.copy()
    myHolds.loc[myHolds.index[0], 'Cash'] = myHolds.loc[myHolds.index[0], 'Cash'] + start_val
    myHolds = myHolds.cumsum()
    # print(myHolds)

    # 4. Prepare Values Data Frame:
    myVals = myPrices * myHolds
    portvals = myVals.sum(axis=1)
    # print(portvals)

    return portvals