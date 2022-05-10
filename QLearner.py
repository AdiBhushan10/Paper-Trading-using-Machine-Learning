""""""
"""  		  	   		  	  			  		 			     			  	 
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  	  			  		 			     			  	 

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

Student Name: Aditya Bhushan 		  	   		  	  			  		 			     			  	 
GT User ID: abhushan30  		  	   		  	  			  		 			     			  	 
GT ID: 903630361  		  	 

-----------REFERENCES---------------------  	
http://incompleteideas.net/sutton/book/RLbook2018.pdf
http://www-anw.cs.umass.edu/~barto/courses/cs687/Chapter%209.pdf 
https://arxiv.org/pdf/1712.01275.pdf 
https://arxiv.org/pdf/cs/9605103.pdf
https://deepmind.com/learning-resources/-introduction-reinforcement-learning-david-silver
https://omscs.gatech.edu/cs-7642-reinforcement-learning-course-videos	  	  			  		 			     			  	 
"""

import random as rand

import numpy as np


class QLearner(object):
    """
    This is a Q learner object.

    :param num_states: The number of states to consider.
    :type num_states: int
    :param num_actions: The number of actions available..
    :type num_actions: int
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.
    :type alpha: float
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.
    :type gamma: float
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.
    :type rar: float
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.
    :type radr: float
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.
    :type dyna: int
    :param verbose: If “verbose” is True, your code can print out information for debugging.
    :type verbose: bool
    """

    def author(self):
        return "abhushan30"

    def __init__(self,
                 num_states=100, \
                 num_actions=4, \
                 alpha=0.2, \
                 gamma=0.9, \
                 rar=0.5, \
                 radr=0.99, \
                 dyna=0, \
                 verbose=False):
        """
        Constructor method
        """
        rand.seed(903630361) # My GT ID
        self.verbose = verbose
        self.num_actions = num_actions
        self.alpha, self.gamma = alpha, gamma
        self.rar, self.radr, self.dyna  = rar, radr, dyna
        self.sy = []
        self.ay = []
        self.spy = []
        self.ry = []
        self.s = 0
        self.a = 0
        self.Q = np.random.uniform(-1.0, 1.0, size=(num_states, num_actions))
        self.num_states = num_states

    def querysetstate(self, s):

        """
        Update the state without updating the Q-table

        :param s: The new state
        :type s: int
        :return: The selected action
        :rtype: int
        """
        self.s = s
        #rand.seed(903630361) # My GT ID
        #action = rand.randint(0, self.num_actions - 1)
        var = rand.random()
        if var < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.Q[s])

        if self.verbose:
            print(f"s = {s}, a = {action}")
        return action

    def query(self, s_prime, r):
        """
        Update the Q table and return an action

        :param s_prime: The new state
        :type s_prime: int
        :param r: The immediate reward
        :type r: float
        :return: The selected action
        :rtype: int
        """
        # Q-Table updates
        al, gm = self.alpha, self.gamma
        self.Q[self.s, self.a] = ((1 - al) * self.Q[self.s, self.a]) + (
                    al * (r + (gm * self.Q[s_prime, np.argmax(self.Q[s_prime])])))

        self.sy.append(self.s)
        self.ay.append(self.a)
        self.spy.append(s_prime)
        self.ry.append(r)

        # Dyna Implementation (experience replays)
        dyna_idx = np.random.randint(len(self.sy), size=self.dyna)
        for i in range(self.dyna):
            dind = dyna_idx[i]
            sdyna = self.sy[dind]
            adyna = self.ay[dind]
            spdyna = self.spy[dind]
            rdyna = self.ry[dind]
            self.Q[sdyna, adyna] = ((1 - al) * self.Q[sdyna, adyna]) + (
                        al * (rdyna + (gm * self.Q[spdyna, np.argmax(self.Q[spdyna])])))

        # rand.seed(903630361) # My GT ID
        var = rand.random()
        if var < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.Q[s_prime])

        # This is to update action, sprome and learning rate
        self.a,self.s = action, s_prime
        self.rar = self.rar*self.radr

        if self.verbose:
            print(f"s = {s_prime}, a = {action}, r={r}")
        return action


if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him")