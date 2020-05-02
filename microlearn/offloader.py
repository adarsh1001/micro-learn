
class Offload:
    supported_algorithms = ["LinearDiscriminantAnalysis", "QuadraticDiscriminantAnalysis", "GaussianNB", "SVC"]

    def __init__(self):
        self.model = None
        self.offloader = None
        self.algorithm = None

    def get_algorithm(self, model):
        return model.__repr__().split('(')[0]

    def is_algorithm_supported(self, model):
        try:
            model.__getstate__()
        except AttributeError:
            return False
        if "_sklearn_version" not in model.__getstate__():
            return False
        algorithm = self.get_algorithm(model)
        return algorithm in self.supported_algorithms
    
    def is_model_trained(self, model):
        try:
            model.__dict__["classes_"]
        except KeyError:
            return False
        if len(model.__dict__["classes_"]) != 2:
            return False
        return True

    def offload(self, model):
        if self.is_algorithm_supported(model):
            self.algorithm = self.get_algorithm(model)
        else:
            raise TypeError("Input ML model not supported! Only LDA, QDA, GNB and SVM of scikit-learn are supported.")

        if self.is_model_trained(model):
            self.model = model
        else:
            raise TypeError("Input ML model not trained on a binary-labelled dataset! First fit() on the dataset and then offload.")


