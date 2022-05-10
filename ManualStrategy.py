""""""
"""Project 8: Manual STRATEGY	  	   		  	  			  		 			     			  	 

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
import matplotlib.pyplot as myPlot
import indicators as I
import marketsimcode as mktsmcd


def author():
    return "abhushan30"


def testPolicy(
        symbol='AAPL',
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=100000
):
    myDates = pd.date_range(sd, ed)
    myPrices = get_data([symbol], myDates)
    # get_Data add SPY which we do not want
    if 'SPY' != [symbol]:
        myPrices.drop('SPY', axis=1, inplace=True)
    # Case when we have incomplete data or missing values
    myPrices = myPrices.fillna(method="ffill").fillna(method="bfill")

    commission = 9.95  # specified on project page
    impact = 0.005  # specified on project page
    slbWindow = 20
    myNormPrices = myPrices / myPrices.iloc[0, :]
    orders = pd.DataFrame(0, index=myNormPrices.index, columns=['Order', 'Shares', symbol])

    _, priceSma, motm, bbper = I.myIndicators(myNormPrices, symbol=symbol, sd=sd,
                                                     ed=ed, lookback=slbWindow)

    action, counter, myInvestment = 0, 1, 1000
    for idx, vals in myNormPrices.iterrows():
        if (counter - slbWindow) > 0:    #Loop begins after the 1st sliding lookback window
            if priceSma.loc[idx][0]< 0.9 and bbper.loc[idx][0]< 0.2  and motm.loc[idx][0]< -0.1  and action < myInvestment:
                orders.loc[idx]['Order'] = 'BUY'
                #orders, action = share_allocation(orders.loc[idx]['Order'], idx, symbol, orders, action)
                if action == 0:
                    orders.loc[idx]['Shares'] = myInvestment
                    orders.loc[idx][symbol] = myInvestment
                else:
                    orders.loc[idx]['Shares'] = 2 * myInvestment
                    orders.loc[idx][symbol] = 2 * myInvestment
                action = myInvestment
            elif priceSma.loc[idx][0]> 0.9 and bbper.loc[idx][0]> 0.8  and motm.loc[idx][0]< 0.1  and action > (-1*myInvestment):
                orders.loc[idx]['Order'] = 'SELL'
                #orders, action = share_allocation(orders.loc[idx]['Order'], idx, symbol, orders, action)
                if action == 0:
                    orders.loc[idx]['Shares'] = myInvestment
                    orders.loc[idx][symbol] = -1 * myInvestment
                else:
                    orders.loc[idx]['Shares'] = 2 * myInvestment
                    orders.loc[idx][symbol] = -2 * myInvestment
                action = -1* myInvestment
        counter = counter + 1
    trades = orders.drop(columns=['Order', 'Shares'])
    return trades

"""
def share_allocation(signal, idx, symbol, orders, action):
    if signal == 'buy':
        if action == 0:
            orders.loc[idx]['Shares'] = 1000
            orders.loc[idx][symbol] = 1000
        else:
            orders.loc[idx]['Shares'] = 2000
            orders.loc[idx][symbol] = 2000
        action = 1000
    else:
        if action == 0:
            orders.loc[idx]['Shares'] = 1000
            orders.loc[idx][symbol] = -1000
        else:
            orders.loc[idx]['Shares'] = 2000
            orders.loc[idx][symbol] = -2000
        action = -1000
    return orders, action
"""

def stats_and_plot(
    symbol,
    myPerfTitle,
    sd,
    ed,
    sv=100000,
    commission=0.0,
    impact=0.0,
):
    myTrades = testPolicy(symbol, sd, ed, sv) #,commission,impact)
    # Orders table for my portfolio
    myOrders = myTrades.copy()
    myOrders['Shares'] = np.absolute(myOrders[symbol])
    myOrders['Symbol'] = symbol
    myOrders['Order'] = np.where(myOrders[symbol] < 0, 'SELL', 'NO TRADE')
    myOrders['Order'] = np.where(myOrders[symbol] > 0, 'BUY', 'NO TRADE')
    myportVals = mktsmcd.compute_portvals(myOrders)
    # normPortVals = myportVals/myportVals.iloc[0]

    # Orders table for benchmarking
    myOrd, mySym = ['BUY', 'SELL'], [symbol,symbol]
    min, max = myTrades.index.min(), myTrades.index.max()
    benchOrder = pd.DataFrame(data={'Symbol': mySym, 'Order': myOrd, 'Shares': [1000, -1000]}, index={min, max})
    mybenchmarkVals = mktsmcd.compute_portvals(benchOrder)
    # normBenchVals = mybenchmarkVals/mybenchmarkVals.iloc[0]

    # Testing benchmark statistics
    dFrm_bch = mybenchmarkVals.copy()
    dRet_bch = dFrm_bch / dFrm_bch.shift(1) - 1
    dRet_bch.iloc[0] = 0.0
    cum_ret_bch = (mybenchmarkVals[-1] / mybenchmarkVals[0]) - 1
    avg_daily_ret_bch, std_daily_ret_bch = dRet_bch.mean(), dRet_bch.std()
    sharpe_ratio_bch = np.sqrt(252) * (avg_daily_ret_bch / std_daily_ret_bch)

    # Testing my portfolio statistics
    dFrm = myportVals.copy()
    dRet = dFrm / dFrm.shift(1) - 1
    dRet.iloc[0] = 0.0
    cum_ret = (myportVals[-1] / myportVals[0]) - 1
    avg_daily_ret, std_daily_ret = dRet.mean(), dRet.std()
    sharpe_ratio = np.sqrt(252) * (avg_daily_ret / std_daily_ret)

    # Compare Manual Strategy against Benchmarking
    print(f"Date Range: {sd} to {ed}")
    print()
    print(f"Sharpe Ratio - Manual Strategy: {sharpe_ratio}")
    print(f"Sharpe Ratio - Benchmarking: {sharpe_ratio_bch}")
    print()
    print(f"Cumulative Return - Manual Strategy: {cum_ret}")
    print(f"Cumulative Return - Benchmarking: {cum_ret_bch}")
    print()
    print(f"Standard Deviation - Manual Strategy: {std_daily_ret}")
    print(f"Standard Deviation - Benchmarking: {std_daily_ret_bch}")
    print()
    print(f"Average Daily Return - Manual Strategy: {avg_daily_ret}")
    print(f"Average Daily Return - Benchmarking: {avg_daily_ret_bch}")
    print()
    print(f"Final Portfolio Value - Manual Strategy: {myportVals[-1]}")
    print(f"Final Portfolio Value - Benchmarking: {mybenchmarkVals[-1]}")

    # My plot for TOS Strategy as compared to the Benchmarking Strategy
    normPortVals, normBenchVals = myportVals / myportVals.iloc[0], mybenchmarkVals / mybenchmarkVals.iloc[0]
    myPlot.figure(figsize=(10, 6))
    myPlot.plot(normPortVals, label="Manual Strategy", color='red')
    myPlot.plot(normBenchVals, label="Benchmarking", color='purple')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Normalized Portfolio Values')
    for idx, vals in myTrades.iterrows():
        if myTrades.loc[idx][symbol] < 0:
            myPlot.axvline(x=idx, color='k', linestyle='dashdot', alpha=0.7)
        elif myTrades.loc[idx][symbol] > 0:
            myPlot.axvline(x=idx, color='b', linestyle='dashdot', alpha=0.7)
    myPlot.legend(['Manual', "Benchmark", "Short", "Long"])
    #myPlot.legend()
    myPlot.title('Strategy Comparison - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.savefig('Manual Strategy - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.close()


if __name__ == "__main__":
    symbol = 'JPM'
    comm,imp = 9.95,0.005

    # MY INSAMPLE STATISTICS
    sdin, edin = dt.datetime(2008,1,1),dt.datetime(2009,12,31)
    stats_and_plot(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=imp)

    # MY OUTSAMPLE STATISTICS
    sdout, edout = dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)
    stats_and_plot(symbol,'Out Sample Performance',sdout,edout,100000,commission=comm,impact=imp)
