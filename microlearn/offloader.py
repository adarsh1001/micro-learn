from .ml_models.SVC import OffloadSVM
from .ml_models.GaussianNB import OffloadGNB
from .ml_models.LinearRegression import OffloadLR
from .ml_models.Perceptron import OffloadPerceptron
from .ml_models.LogisticRegression import OffloadLogit
from .ml_models.LinearDiscriminantAnalysis import OffloadLDA
from .ml_models.QuadraticDiscriminantAnalysis import OffloadQDA

class Offload:
    supported_algorithms = ["LinearDiscriminantAnalysis", "QuadraticDiscriminantAnalysis", "GaussianNB", "SVC", "LinearSVC", "Perceptron", "LinearRegression", "LogisticRegression"]

    def __init__(self, model, optional=None):
        self.optional = optional
        self.check_model_validity(model)
        self.model = model
        self.algorithm = self.get_algorithm(model)
        self.offloader = self.get_offloader()

    def get_algorithm(self, model):
        return model.__repr__().split('(')[0]

    def is_algorithm_supported(self, model):
        try:
            model.__getstate__()
        except AttributeError:
            return False
        if "_sklearn_version" not in model.__getstate__():
            return False
        return self.get_algorithm(model) in self.supported_algorithms
    
    def is_model_trained(self, model):
        if self.get_algorithm(model) == "StandardScaler":
            return "n_samples_seen_" in model.__dict__
        elif self.get_algorithm(model) == "LinearRegression":
            return "singular_" in model.__dict__
        else:
            return "classes_" in model.__dict__

    def is_model_binary(self, model):
        if self.get_algorithm(model) == "LinearRegression":
            return True
        else:
            return len(model.__dict__["classes_"]) == 2

    def get_offloader(self):
        if self.algorithm == self.supported_algorithms[0]:  #LDA
            return OffloadLDA(self.model)     
        elif self.algorithm == self.supported_algorithms[1]:  #QDA
            return OffloadQDA(self.model)
        elif self.algorithm == self.supported_algorithms[2]: #GNB
            return OffloadGNB(self.model)
        elif self.algorithm == self.supported_algorithms[3] or self.algorithm == self.supported_algorithms[4]: #SVM
            return OffloadSVM(self.model, self.optional)
        elif self.algorithm == self.supported_algorithms[5]: #Perceptron
            return OffloadPerceptron(self.model)
        elif self.algorithm == self.supported_algorithms[6]: #LR
            return OffloadLR(self.model)
        elif self.algorithm == self.supported_algorithms[7]: #LogR
            return OffloadLogit(self.model)
    
    def check_model_validity(self, model):
        if not self.is_algorithm_supported(model):
            raise TypeError("Input ML model not supported! Only LDA, QDA, GNB, LR, LogR, SVM and Perceptron of scikit-learn are supported.")

        if not self.is_model_trained(model):
            raise TypeError("Input ML model not trained on a dataset! First .fit() on a dataset and then offload.")

        if not self.is_model_binary(model):
            raise TypeError("Input ML model trained on a multiclass dataset! Only binary-class models are supported.")

        if self.get_algorithm(model) == "SVC" or self.get_algorithm(model) == "LinearSVC":
            if self.get_algorithm(self.optional) != "StandardScaler":
                raise TypeError("SVM algorithm is scale-variant and requires StandardScaler variable as the second argument.")
            if not self.is_model_trained(self.optional):
                raise TypeError("First fit StandardScaler on the training dataset and then offload.")

    def get_params(self):
        return self.offloader.get_params()

    def export_to_arduino(self, path):
        preamble = "//This code was autogenerated using micro-learn.\n//Use the dummy variable array 'data' to interact with the ML inference.\n\n"
        code = preamble + self.offloader.get_arduino_code()

        f = open(path, 'a')
        f.write(code)
        f.close()





