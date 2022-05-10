# Project Assess Learners
# Implement a Random Tree Learner using JR Quinlan Algorithm but using random choice instead of correlation function
import numpy as np

class RTLearner(object):
    """
    This is a Random Tree Learner. It is implemented correctly.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool

    :param leaf_size: a hyperparameter that defines the maximum number of samples to be aggregated at a leaf
    :type verbose: int (1 or 50)
    """

    def __init__(self, leaf_size = 1, verbose=False):
        """
        Constructor method
        """
        self.leaf_size, self.verbose = leaf_size, verbose
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
        # I will combine the data from data_x & data_y and then send it to my build tree function
        self.final_tree = self.build_tree(data_x,data_y)
        #self.final_tree = self.build_tree(np.hstack((data_x, np.array([data_y]).T)))

        #print("COMPLETE!!!")

        #Show tree when verbose is True
        if self.verbose: print(self.final_tree)
        return self.final_tree

    def build_tree(self,data_x,data_y):
        # Unpack combined data
        ydata, xdata = data_y, data_x # data[:, -1], data[:, :-1]
        # print(ydata.shape)
        # Stopping Criteria(s):
        if ydata.shape[0] == 1:
            my_arr = np.array([-1, ydata[0], np.nan, np.nan], dtype=object)
            return my_arr
        if xdata.shape[0] <= self.leaf_size:
            my_arr = np.array([-1, np.mean(ydata), np.nan, np.nan], dtype=object)
            return my_arr
        if np.allclose(ydata, ydata[0]):
            my_arr = np.array([-1, ydata[0], np.nan, np.nan], dtype=object)
            return my_arr
        else:
            #determine best feature (i) to split on using a random choice
            idx = np.random.choice(xdata.shape[1])  #random value ith from total columns in xdata
            split_val = np.median(xdata[:,idx])
            if (xdata.shape[0] == (xdata[xdata[:,idx] > split_val]).shape[0]) or (xdata.shape[0] == (xdata[xdata[:, idx] <= split_val]).shape[0]):
                my_arr = np.array([[-1,np.mean(ydata),np.nan, np.nan]], dtype=object)
                return my_arr
            # Recursion logic
            left_tree = self.build_tree(xdata[xdata[:,idx] <= split_val],ydata[xdata[:,idx] <= split_val]) #self.build_tree(data[data[:,idx] <= split_val])
            right_tree = self.build_tree(xdata[xdata[:,idx] > split_val],ydata[xdata[:,idx] > split_val]) #self.build_tree(data[data[:,idx] > split_val])
            if len(np.shape(left_tree)) == 1: root = np.array([[idx,split_val, 1, 2]])
            else: root = np.array([[idx,split_val, 1, left_tree.shape[0]+1]])
            final_tree = np.vstack((root, left_tree, right_tree))
            return final_tree

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        final_pred = []
        my_pred_arr = np.array([])
        if points.ndim==1: points.shape[0] = 1
        for row in range(points.shape[0]):  # Number of rows in points
            idx = 0
            while self.final_tree[idx,0] != -1: # and idx <= points.shape[0]:   # While continues till we reach leaf idx
                if points.shape[0] == 1:
                    if points[int(self.final_tree[idx,0])] <= self.final_tree[idx,1]: idx += int(self.final_tree[idx, 2])
                    else: idx += int(self.final_tree[idx, 3])
                else:
                    if points[row, int(self.final_tree[idx,0])] <= self.final_tree[idx,1]: idx += int(self.final_tree[idx,2])
                    else: idx += int(self.final_tree[idx,3])
                predict_val = self.final_tree[idx,1]
            final_pred.append(predict_val)
        my_pred_arr = np.array(final_pred, dtype=object)

        #Show tree when verbose is True
        if self.verbose: print(my_pred_arr)
        return my_pred_arr

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
