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
        str_w = ', '.join([str(x) for x in self.w])

        code = f"""double w[] = {{{str_w}}};
double c = {str(self.c)};

void setup() {{
	Serial.begin(9600);

}}

void loop() {{
	//Data Section: To Be Coded Manually

	float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

	//ML Inference Section

	double temp = 0.0;
	for(int i=0; i<{str(self.dim)}; i++)
	{{
		temp += data[i]*w[i];
	}}

	if(temp >= c)
	{{
		//Do something for class label 1.
		Serial.println("1.0");
	}}
	else
	{{
		//Do something for class label 0.
		Serial.println("0.0"); 
	}}

	delay(1000);
}}"""
        return code



    