import math
import numpy as np 

class OffloadQDA:
    def __init__(self, model):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        try:
            self.cov_matrix0 = model.covariance_[0]
            self.cov_matrix1 = model.covariance_[1]
        except AttributeError:
            print("QDA must be trained with 'store_covariances=True' parameter.")
            raise
        self.inv_cov_matrix0 = np.linalg.inv(self.cov_matrix0)
        self.inv_cov_matrix1 = np.linalg.inv(self.cov_matrix1)
        self.mean_vector0 = model.means_[0]
        self.mean_vector1 = model.means_[1]
        self.prior0 = model.priors_[0]
        self.prior1 = model.priors_[1]
        self.dim = len(self.mean_vector0)

        self.w = self.get_weights()
        self.c = self.get_constant()
        self.invEdiff = self.get_cov_matrix_diff()

    def get_weights(self):
        term1 = 2*np.matmul(self.inv_cov_matrix1, self.mean_vector1)
        term2 = 2*np.matmul(self.inv_cov_matrix0, self.mean_vector0)
        return term1 - term2
    
    def get_cov_matrix_diff(self):
        return self.inv_cov_matrix0 - self.inv_cov_matrix1
    
    def get_constant(self):
        term1_num = self.prior0*math.sqrt(np.linalg.det(self.cov_matrix1))
        term1_den = self.prior1*math.sqrt(np.linalg.det(self.cov_matrix0))
        term1 = 2*math.log(term1_num/term1_den)

        term2 = np.matmul(np.matmul(self.mean_vector1, self.inv_cov_matrix1), self.mean_vector1)

        term3 = np.matmul(np.matmul(self.mean_vector0, self.inv_cov_matrix0), self.mean_vector0)

        return term1 + term2 - term3

    def get_params(self):
        return {'Inverse_CovMatrix_Diff':self.invEdiff, 'Weight_Vector':self.w, 'Constant':self.c}

    def get_arduino_code(self):
        invEdiff_terms = []
        for term in self.invEdiff:
            temp = '{' +  ', '.join([str(x) for x in term]) + '}'
            invEdiff_terms.append(temp)
        str_invEdiff = ', '.join(invEdiff_terms)

        str_w = ', '.join([str(x) for x in self.w])

        code = f"""double invEdiff[{str(self.dim)}][{str(self.dim)}] = {{{str_invEdiff}}};
double w[] = {{{str_w}}};
double c = {str(self.c)};

void setup() {{
    Serial.begin(9600);

}}

void loop() {{
    //Data Section: To Be Coded Manually

    float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

    //ML Inference Section

    double term = 0.0;
    for(int col=0; col<{str(self.dim)}; col++)
    {{
        double temp = 0.0;
        for(int i=0; i<{str(self.dim)}; i++)
        {{
            temp += data[i] * invEdiff[i][col];
        }}
        term += (temp + w[col]) * data[col];
    }}

    if(term >= c)
    {{
        //Do something for class label {str(self.class1)}.
        Serial.println("{str(self.class1)}");
    }}
    else
    {{
        //Do something for class label {str(self.class0)}.
        Serial.println("{str(self.class0)}"); 
    }}

    delay(1000);
}}"""
        return code

