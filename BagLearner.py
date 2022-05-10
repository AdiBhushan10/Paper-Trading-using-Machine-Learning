# Project Assess Learners
# Implement a BagLearner

import numpy as np


class BagLearner(object):
    """
    This is a Bag Learner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, learner, kwargs={"leaf_size": 1}, bags=20, boost=False, verbose=False):
        """
        Constructor method
        """
        self.kwargs, self.verbose, self.bags, self.boost = kwargs, verbose, bags, boost
        self.learner = [learner(**self.kwargs) for bag in range(self.bags)]
        #pass  # move along, these aren't the drones you're looking for

    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "abhushan30"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        idx = np.random.choice(data_x.shape[0],size=data_x.shape[0],replace=True)
        # I will combine the data from data_x & data_y and then send it through my build tree function
        self.final_tree = [self.learner[bag].add_evidence(data_x[idx],data_y[idx]) for bag in range(self.bags)]
        #Show tree when verbose is True
        if self.verbose:
            print(self.final_tree)
        return self.final_tree

    def query(self, points):
        """
        Estimate a set of test points given the model we built.
        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        """
        my_pred_arr = np.array([]) #empty array
        #bag_inv = 1.0/self.bags
        #my_pred_arr = bag_inv * np.sum(np.array([lrn.query(points) for lrn in self.learner]), axis = 0)
        #x = np.array([lrn.query(points) for lrn in self.learner])
        #vals, counts = np.unique(x, return_counts=True)
        my_pred_arr = np.unique(np.array([lrn.query(points) for lrn in self.learner]), return_counts=False) #vals #stats.mode(np.array([lrn.query(points) for lrn in self.learner]))[0]
        #Show tree when verbose is True
        if self.verbose:
            print(my_pred_arr)
        return my_pred_arr



if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
