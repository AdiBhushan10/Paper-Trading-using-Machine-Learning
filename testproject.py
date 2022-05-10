""""""
"""Project 8: TEST PROJECT	  	   		  	  			  		 			     			  	 

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
import ManualStrategy as manStr, StrategyLearner as strLrn, experiment1 as expA, experiment2 as expB
import QLearner as Q
import random as rand

def author():
    return "abhushan30"

if __name__ == "__main__":
    rand.seed(903630361)  # My GT ID
    symbol = 'JPM'
    comm,imp = 9.95,0.005
    sv = 100000

    # Manual Strategy Vs Benchmark
    # MY INSAMPLE STATISTICS
    sdin, edin = dt.datetime(2008,1,1),dt.datetime(2009,12,31)
    manStr.stats_and_plot(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=imp)

    # MY OUTSAMPLE STATISTICS
    sdout, edout = dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)
    manStr.stats_and_plot(symbol,'Out Sample Performance',sdout,edout,100000,commission=comm,impact=imp)

    # Experiment 1: COMPARISON
    #expA()
    # MY INSAMPLE STATISTICS
    sdin, edin = dt.datetime(2008,1,1),dt.datetime(2009,12,31)
    expA.experiment1(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact=imp)
    # MY OUTSAMPLE STATISTICS
    sdout, edout = dt.datetime(2010, 1, 1), dt.datetime(2011, 12, 31)
    expA.experiment1(symbol,'Out Sample Performance',sdout,edout,100000,commission=comm,impact=imp)

    # Experiment 2: IMPACT and STRATEGY LEARNER
    #expB()
    comm = 0.0
    impact1, impact2, impact3 = 0.005, 0.25, 0.0
    expB.experiment2(symbol,'In Sample Performance',sdin,edin,100000,commission=comm,impact1=impact1, impact2=impact2,impact3=impact3)


