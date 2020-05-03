from .ml_models.LinearDiscriminantAnalysis import OffloadLDA

class Offload:
    supported_algorithms = ["LinearDiscriminantAnalysis", "QuadraticDiscriminantAnalysis", "GaussianNB", "SVC"]

    def __init__(self, model):
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
        algorithm = self.get_algorithm(model)
        return algorithm in self.supported_algorithms
    
    def is_model_trained(self, model):
        try:
            model.__dict__["classes_"]
        except KeyError:
            return False
        return True

    def is_model_binary(self, model):
        return len(model.__dict__["classes_"]) == 2

    def get_offloader(self):
        if self.algorithm == self.supported_algorithms[0]:  #LDA
            return OffloadLDA(self.model)     
    
    def check_model_validity(self, model):
        if self.is_algorithm_supported(model):
            self.algorithm = self.get_algorithm(model)
        else:
            raise TypeError("Input ML model not supported! Only LDA, QDA, GNB and SVM of scikit-learn are supported.")

        if not self.is_model_trained(model):
            raise TypeError("Input ML model not trained on a dataset! First .fit() on a dataset and then offload.")

        if not self.is_model_binary(model):
            raise TypeError("Input ML model trained on a multiclass dataset! Only binary-class models are supported.")

    def get_params(self):
        return self.offloader.get_params()

    def export_to_arduino(self, model):
        pass


