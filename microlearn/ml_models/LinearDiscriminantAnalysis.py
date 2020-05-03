import math
import numpy as np

class OffloadLDA:
    def __init__(self, model):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        try:
            self.cov_matrix = model.covariance_
        except AttributeError:
            print("LDA must be trained with 'store_covariances=True' parameter.")
            raise
        self.inv_cov_matrix = np.linalg.inv(self.cov_matrix)
        self.mean_vector0 = model.means_[0]
        self.mean_vector1 = model.means_[1]
        self.prior0 = model.priors_[0]
        self.prior1 = model.priors_[1]
        self.dim = len(self.mean_vector0)

        self.w = self.get_weights()
        self.c = self.get_intercept()

    def get_weights(self):
        return np.matmul(self.inv_cov_matrix, (self.mean_vector1 - self.mean_vector0))

    def get_intercept(self):
        term1 = math.log(self.prior0/self.prior1)
        term2 = 0.5*(np.matmul(np.matmul(self.mean_vector0, self.inv_cov_matrix), self.mean_vector0) - np.matmul(np.matmul(self.mean_vector1, self.inv_cov_matrix), self.mean_vector1))
        return term1 - term2
    
    def get_params(self):
        return {'Weight_Vector':self.w, 'Intercept_Constant':self.c}

    def get_arduino_code(self):
        global_section = "double w[] = {"
        #Offload weight vector
        for val in self.w:
            global_section += str(val)
            global_section += ", "
        global_section = global_section[:-2]
        global_section += "};\n"
        #Offload intercept constant
        global_section += "double c = " + str(self.c) + ";\n\n"

        setup_section = "void setup() {\n\tSerial.begin(9600);\n\n}\n\n"

        loop_section =  "void loop() {\n\t//Data Section: To Be Coded Manually\n\n\tfloat data[" + str(self.dim) + "]; //This is your feature vector. Retrive your data into this array\n\n"
        #Inference steps
        loop_section += "\t//ML Inference Section\n\n\tdouble temp = 0.0;\n\tfor(int i=0; i<" + str(self.dim) + "; i++)\n\t{\n"
        loop_section += "\t\ttemp += data[i]*w[i];\n\t}\n\n"
        #Label 1
        loop_section += '\tif(temp >= c)\n\t{\n\t\t//Do something for class label 1\n\t\tSerial.println("' + str(self.class1) + '");\n\t}\n'
        #Label 0
        loop_section += '\telse\n\t{\n\t\t//Do something for class label 0\n\t\tSerial.println("' + str(self.class0) + '"); \n\t}\n\n'
        loop_section += "\tdelay(1000);\n}"

        code = global_section + setup_section + loop_section
        return code



    