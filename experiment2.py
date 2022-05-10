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

def experiment2(
    symbol,
    myPerfTitle,
    sd,
    ed,
    sv=100000,
    commission=0.0,
    impact1=0.0,
    impact2=0.0,
    impact3=0.0
):

    # Preparing my learner from Strategy Learner
    myLearn = strLrn.StrategyLearner(impact=impact1)
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
    myportValsSL1 = mktsmcd.compute_portvals(myNewOrders,sv,commission,impact1)

    # Testing my strategy learner statistics
    dFrmSL = myportValsSL1.copy()
    dRetSL = dFrmSL / dFrmSL.shift(1) - 1
    dRetSL.iloc[0] = 0.0
    cum_retSL = (myportValsSL1[-1] / myportValsSL1[0]) - 1
    avg_daily_retSL, std_daily_retSL = dRetSL.mean(), dRetSL.std()
    sharpe_ratioSL = np.sqrt(252) * (avg_daily_retSL / std_daily_retSL)

    # Compare Manual Strategy against Benchmarking
    print(f"Date Range: {sd} to {ed}")
    print(f"Sharpe Ratio - Impact1 on SL: {sharpe_ratioSL}")
    print(f"Cumulative Return - Impact1 on SL: {cum_retSL}")
    print(f"Standard Deviation - Impact1 on SL: {std_daily_retSL}")
    print(f"Average Daily Return - Impact1 on SL: {avg_daily_retSL}")
    print(f"Final Portfolio Value - Impact1 on SL: {myportValsSL1[-1]}")



    # Preparing my learner from Strategy Learner
    myLearn = strLrn.StrategyLearner(impact=impact2)
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
    myportValsSL2 = mktsmcd.compute_portvals(myNewOrders,sv,commission,impact2)

    # Testing my strategy learner statistics
    dFrmSL = myportValsSL2.copy()
    dRetSL = dFrmSL / dFrmSL.shift(1) - 1
    dRetSL.iloc[0] = 0.0
    cum_retSL = (myportValsSL2[-1] / myportValsSL2[0]) - 1
    avg_daily_retSL, std_daily_retSL = dRetSL.mean(), dRetSL.std()
    sharpe_ratioSL = np.sqrt(252) * (avg_daily_retSL / std_daily_retSL)

    # Compare Manual Strategy against Benchmarking
    print(f"Date Range: {sd} to {ed}")
    print(f"Sharpe Ratio - Impact2 on SL: {sharpe_ratioSL}")
    print(f"Cumulative Return - Impact2 on SL: {cum_retSL}")
    print(f"Standard Deviation - Impact2 on SL: {std_daily_retSL}")
    print(f"Average Daily Return - Impact2 on SL: {avg_daily_retSL}")
    print(f"Final Portfolio Value - Impact2 on SL: {myportValsSL2[-1]}")


    # Preparing my learner from Strategy Learner
    myLearn = strLrn.StrategyLearner(impact=impact3)
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
    myportValsSL3 = mktsmcd.compute_portvals(myNewOrders,sv,commission,impact3)

    # Testing my strategy learner statistics
    dFrmSL = myportValsSL3.copy()
    dRetSL = dFrmSL / dFrmSL.shift(1) - 1
    dRetSL.iloc[0] = 0.0
    cum_retSL = (myportValsSL3[-1] / myportValsSL3[0]) - 1
    avg_daily_retSL, std_daily_retSL = dRetSL.mean(), dRetSL.std()
    sharpe_ratioSL = np.sqrt(252) * (avg_daily_retSL / std_daily_retSL)

    # Compare Manual Strategy against Benchmarking
    print(f"Date Range: {sd} to {ed}")
    print(f"Sharpe Ratio - Impact3 on SL: {sharpe_ratioSL}")
    print(f"Cumulative Return - Impact3 on SL: {cum_retSL}")
    print(f"Standard Deviation - Impact3 on SL: {std_daily_retSL}")
    print(f"Average Daily Return - Impact3 on SL: {avg_daily_retSL}")
    print(f"Final Portfolio Value - Impact3 on SL: {myportValsSL3[-1]}")

    normPortVals1, normPortVals2, normPortVals3 = myportValsSL1 / myportValsSL1.iloc[0], myportValsSL2 / myportValsSL2.iloc[0],myportValsSL3 / myportValsSL3.iloc[0]

    # My plot for TOS Strategy as compared to the Benchmarking Strategy
    myPlot.figure(figsize=(8, 6))
    myPlot.plot(normPortVals1, color='red')
    myPlot.plot(normPortVals2, color='purple')
    myPlot.plot(normPortVals3, color='blue')
    myPlot.xlabel('Dates')
    myPlot.ylabel('Normalized Portfolio Values')
    myPlot.legend(['Impact1', 'Impact2', 'Impact3'])
    myPlot.title('Market Impact on SL - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.savefig('Experiment 2 - ' + str(symbol) + ' stock - ' + str(myPerfTitle))
    myPlot.close()


if __name__ == "__main__":
    rand.seed(903630361)  # My GT ID
    symbol = 'JPM'
    comm = 0.0
    impact1, impact2, impact3 = 0.005, 0.25, 0.08

    # MY STATISTICS
    sdin, edin = dt.datetime(2008,1,1),dt.datetime(2009,12,31)
    experiment2(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact1=impact1, impact2=impact2,impact3=impact3)
    #experiment2(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=impact2)
    #xperiment2(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=impact3)

