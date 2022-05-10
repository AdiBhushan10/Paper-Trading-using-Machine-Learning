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
import pandas as pd
import util as ut
import random as rand
import QLearner as ql
import indicators as I
import marketsimcode as mktsmcd

class StrategyLearner(object):

    def author(self):
        return "abhushan30"

    # constructor
    def __init__(self, verbose=False, impact=0.0):
        self.impact = impact
        self.verbose = verbose
        rand.seed(903630361) # My GT ID
        self.learner = ql.QLearner(num_states=96, \
                                   num_actions=3, \
                                   alpha=0.2, \
                                   gamma=0.99, \
                                   rar=0.9, \
                                   radr=0.99, \
                                   dyna=0, \
                                   verbose=False)

    def add_evidence(self, symbol="IBM", \
                    sd=dt.datetime(2008, 1, 1), \
                    ed=dt.datetime(2009, 1, 1), \
                    sv=10000):
        smaPrice, motm, bbper = convertDiscrete(sd, ed, symbol)
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        myDFrame= ut.get_data(syms, dates)
        prices = myDFrame[syms]
        myPrices = prices.ffill().bfill()
        myTrades = myDFrame[['SPY']]
        myTrades = myTrades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
        myTrades[:] = 0
        dates = myPrices.index

        # TRAINING PHASE
        nowPos,oldPos = 0,0
        nowVal, oldVal = sv, sv

        for i in range(1, len(dates)):
            now,old = dates[i], dates[i - 1]
            s_prime = learnerState(nowPos, smaPrice.loc[now], motm.loc[now], bbper.loc[now])
            r = nowPos * myPrices.loc[now].loc[symbol] + nowVal - oldPos * myPrices.loc[now].loc[
                symbol] - oldVal
            move = self.learner.query(s_prime, r)
            if move == 0: trade = -1000 - nowPos
            elif move == 1: trade = -nowPos
            else: trade = 1000 - nowPos
            oldPos = nowPos
            nowPos += trade
            myTrades.loc[now].loc[symbol] = trade
            if trade > 0: impact = self.impact
            else: impact = -1 * self.impact
            oldVal = nowVal
            nowVal += -myPrices.loc[now].loc[symbol] * (1 + impact) * trade

    def testPolicy(self, symbol="IBM", \
                   sd=dt.datetime(2009, 1, 1), \
                   ed=dt.datetime(2010, 1, 1), \
                   sv=10000):
        smaPrice, motm, bbper = convertDiscrete(sd, ed, symbol)
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        myDFrame= ut.get_data(syms, dates)
        prices = myDFrame[syms]
        myPrices, myTrades = prices.ffill().bfill(), myDFrame[['SPY']]
        myTrades = myTrades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
        myTrades[:] = 0
        dates = myPrices.index

        nowPos = 0
        for i in range(1, len(dates)):
            now, old = dates[i],dates[i - 1]
            s_prime = learnerState(nowPos, smaPrice.loc[now], motm.loc[now], bbper.loc[now])
            move = self.learner.querysetstate(s_prime)
            if move == 0: trade = -1000 - nowPos
            elif move == 1: trade = -nowPos
            else: trade = 1000 - nowPos
            nowPos += trade
            myTrades.loc[now].loc[symbol] = trade
        return myTrades

def convertDiscrete(sd, ed, symbol):
    syms = [symbol]
    dates = pd.date_range(sd, ed)
    myDFrame= ut.get_data(syms, dates)
    prices = myDFrame[syms]
    prices = prices.ffill().bfill()
    myNormPrices = prices / prices.iloc[0, :]
    _, smaPrice, motm, bbper = I.myIndicators(myNormPrices, symbol=symbol, sd=sd,
                                                    ed=ed, lookback=20)
    # LOGIC:
    # if Indicator value < price, then 1
    # if Indicator value < price, then 1
    smaPrice = (prices > smaPrice) * 1
    motm = (prices > motm) * 1
    bbper = (prices > bbper) * 1
    return smaPrice, motm, bbper


def learnerState(state, smaPrice, motm, bbper):
    # Total states available - 96 so the combination of indicator and state should always stay between (0,95)
    # 96 states in total, each permutation of indicators + state return between 0 and 95
    # 0,95 = state 0, state 1
    pointer, multiple = 0, 32
    if state == 0: pointer += multiple
    elif state == 1000: pointer += (2*multiple)
    pointer += smaPrice*(multiple*0.5) + motm*(multiple*0.25) + bbper*(multiple*0.125)
    return int(pointer)

'''
if __name__ == "__main__":
    symbol = 'JPM'
    comm,imp = 9.95,0.005
    slbWindow = 20

    learner = StrategyLearner(impact=0.000)
    # MY INSAMPLE
    learner.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # MY OUTSAMPLE
    myTrades = learner.testPolicy(symbol=symbol, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
'''
