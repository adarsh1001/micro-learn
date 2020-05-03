import math
import numpy as np

class OffloadLDA:
    def __init__(self, model):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        self.cov_matrix = model.covariance_
        self.mean_vector0 = model.means_[0]
        self.mean_vector1 = model.means_[1]
        self.prior0 = model.priors_[0]
        self.prior1 = model.priors_[1]

    def get_weights(self):
        pass

    def get_intercept(self):
        pass