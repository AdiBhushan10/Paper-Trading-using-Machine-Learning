""""""
"""Project 8: EXPERIMENT 1	  	   		  	  			  		 			     			  	 

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

import marketsimcode as mktsmcd
import ManualStrategy as manStr, StrategyLearner as strLrn
import QLearner as Q
import random as rand

def author():
    return "abhushan30"

def experiment1(
    symbol,
    myPerfTitle,
    sd,
    ed,
    sv=100000,
    commission=0.0,
    impact=0.0,
):
    com = commission
    imp = impact
    myTrades = manStr.testPolicy(symbol, sd, ed, sv) #,commission,impact)
    #print(myTrades)
    # Orders table for my portfolio
    myOrders = myTrades.copy()
    myOrders['Shares'] = np.absolute(myOrders[symbol])
    myOrders['Symbol'] = symbol
    myOrders['Order'] = np.where(myOrders[symbol] < 0, 'SELL', 'NO TRADE')
    myOrders['Order'] = np.where(myOrders[symbol] > 0, 'BUY', 'NO TRADE')
    # Orders table for my manual portfolio
    myportValsMS = mktsmcd.compute_portvals(myOrders,sv,com,imp) #,sd,ed,symbol,sv,com,imp)
    # normPortValsMS = myportValsMS/myportValsMS.iloc[0]

    # Orders table for benchmarking
    myOrd, mySym = ['BUY', 'SELL'], [symbol,symbol]
    min, max = myTrades.index.min(), myTrades.index.max()
    benchOrder = pd.DataFrame(data={'Symbol': mySym, 'Order': myOrd, 'Shares': [1000, -1000]}, index={min, max})
    mybenchmarkVals = mktsmcd.compute_portvals(benchOrder)
    # normBenchVals = mybenchmarkVals/mybenchmarkVals.iloc[0]

    # Preparing my learner from Strategy Learner
    myLearn = strLrn.StrategyLearner(impact=imp)
    #myLearn = Q.QLearner()
    myLearn.add_evidence(symbol,sd,ed,sv)
    myNewTrades = myLearn.testPolicy(symbol,sd,ed,sv)
    #print(myNewTrades)
    myNewOrders = myNewTrades.copy()
    myNewOrders['Shares'] = np.absolute(myNewOrders[symbol]) #10
    myNewOrders['Symbol'] = symbol
    myNewOrders['Order'] = np.where(myNewOrders[symbol] < 0, 'SELL', 'NO TRADE')
    myNewOrders['Order'] = np.where(myNewOrders[symbol] > 0, 'BUY', 'NO TRADE')
    # Orders table for my manual portfolio
    #myportValsSL = mktsmcd.compute_portvals(myNewOrders, sv, com, imp)
    myportValsSL = mktsmcd.compute_portvals(myNewOrders,sv,com,imp)
    #print(myportValsSL)
    #normPortValsSL = myportValsSL/myportValsSL.iloc[0]

    # Testing benchmark statistics
    dFrm_bch = mybenchmarkVals.copy()
    dRet_bch = dFrm_bch / dFrm_bch.shift(1) - 1
    dRet_bch.iloc[0] = 0.0
    cum_ret_bch = (mybenchmarkVals[-1] / mybenchmarkVals[0]) - 1
    avg_daily_ret_bch, std_daily_ret_bch = dRet_bch.mean(), dRet_bch.std()
    sharpe_ratio_bch = np.sqrt(252) * (avg_daily_ret_bch / std_daily_ret_bch)

    # Testing my manual portfolio statistics
    dFrmMS = myportValsMS.copy()
    dRetMS = dFrmMS / dFrmMS.shift(1) - 1
    dRetMS.iloc[0] = 0.0
    cum_retMS = (myportValsMS[-1] / myportValsMS[0]) - 1
    avg_daily_retMS, std_daily_retMS = dRetMS.mean(), dRetMS.std()
    sharpe_ratioMS = np.sqrt(252) * (avg_daily_retMS / std_daily_retMS)

    # Testing my strategy learner statistics
    dFrmSL = myportValsSL.copy()
    dRetSL = dFrmSL / dFrmSL.shift(1) - 1
    dRetSL.iloc[0] = 0.0
    cum_retSL = (myportValsSL[-1] / myportValsSL[0]) - 1
    avg_daily_retSL, std_daily_retSL = dRetSL.mean(), dRetSL.std()
    sharpe_ratioSL = np.sqrt(252) * (avg_daily_retSL / std_daily_retSL)

    # Compare Manual Strategy against Benchmarking
    print(f"Date Range: {sd} to {ed}")
    print()
    print(f"Sharpe Ratio - Strategy Learner: {sharpe_ratioSL}")
    print(f"Sharpe Ratio - Manual Strategy: {sharpe_ratioMS}")
    print(f"Sharpe Ratio - Benchmarking: {sharpe_ratio_bch}")
    print()
    print(f"Cumulative Return - Strategy Learner: {cum_retSL}")
    print(f"Cumulative Return - Manual Strategy: {cum_retMS}")
    print(f"Cumulative Return - Benchmarking: {cum_ret_bch}")
    print()
    print(f"Standard Deviation - Strategy Learner: {std_daily_retSL}")
    print(f"Standard Deviation - Manual Strategy: {std_daily_retMS}")
    print(f"Standard Deviation - Benchmarking: {std_daily_ret_bch}")
    print()
    print(f"Average Daily Return - Strategy Leaner: {avg_daily_retSL}")
    print(f"Average Daily Return - Manual Strategy: {avg_daily_retMS}")
    print(f"Average Daily Return - Benchmarking: {avg_daily_ret_bch}")
    print()
    print(f"Final Portfolio Value - Strategy Learner: {myportValsSL[-1]}")
    print(f"Final Portfolio Value - Manual Strategy: {myportValsMS[-1]}")
    print(f"Final Portfolio Value - Benchmarking: {mybenchmarkVals[-1]}")

    # My plot for TOS Strategy as compared to the Benchmarking Strategy
    normPortValsManual, normBenchVals, normPortValsStrategy = myportValsMS / myportValsMS.iloc[0], mybenchmarkVals / mybenchmarkVals.iloc[0], myportValsSL / myportValsSL.iloc[0]
    myPlot.figure(figsize=(8, 6))
    myPlot.plot(normPortValsManual, label="Manual Strategy", color='red')
    myPlot.plot(normBenchVals, label="Benchmarking", color='purple')
    myPlot.plot(normPortValsStrategy, label="Strategy Learner", color='blue')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Normalized Portfolio Values')
    myPlot.legend(['Manual Strategy (MS)', "Strategy Learner (SL)"]) #Short", "Long"])
    myPlot.legend(['Manual Strategy (MS)', "Benchmark", "Strategy Learner (SL)"]) #Short", "Long"])
    myPlot.title('Strategy Comparison - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.savefig('Experiment 1 - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.close()


if __name__ == "__main__":
    rand.seed(903630361)  # My GT ID
    symbol = 'JPM'
    comm,imp = 9.95,0.005

    # MY INSAMPLE STATISTICS
    sdin, edin = dt.datetime(2008,1,1),dt.datetime(2009,12,31)
    experiment1(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=imp)

    # MY OUTSAMPLE STATISTICS
    sdout, edout = dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)
    experiment1(symbol,'Out Sample Performance',sdout,edout,100000,commission=comm,impact=imp)
