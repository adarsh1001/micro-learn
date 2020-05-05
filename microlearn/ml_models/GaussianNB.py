import math
import numpy as np 

class OffloadGNB:
    def __init__(self, model):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        self.prior0 = model.class_prior_[0]
        self.prior1 = model.class_prior_[1]
        self.variance_vector0 = model.sigma_[0]
        self.variance_vector1 = model.sigma_[1]
        self.dim = len(self.variance_vector0)

        self.p0 = self.get_inv_variance(0)
        self.p1 = self.get_inv_variance(1)
        self.c  = self.get_constant()
        self.u0 = model.theta_[0]
        self.u1 = model.theta_[1]

    def get_inv_variance(self, label):
        if label == 0:
            return np.array([1/x for x in self.variance_vector0])
        else:
            return np.array([1/x for x in self.variance_vector1])

    def get_constant(self):
        numerator = 1.0
        denominator = 1.0
        for term_num,term_den in zip(self.variance_vector0, self.variance_vector1):
            numerator *= (1/(math.sqrt(term_num)))
            denominator *= (1/(math.sqrt(term_den)))
        numerator *= self.prior0
        denominator *= self.prior1

        return 2*math.log(numerator/denominator)

    def get_params(self):
        return {'Inverse_Variances_0':self.p0, 'Inverse_Variances_1':self.p1, 'Means_0':self.u0, 'Means_1':self.u1, 'Constant':self.c}

    def get_arduino_code(self):
        str_u0 = ', '.join([str(x) for x in self.u0])
        str_u1 = ', '.join([str(x) for x in self.u1])
        str_p0 = ', '.join([str(x) for x in self.p0])
        str_p1 = ', '.join([str(x) for x in self.p1])

        code = f"""double u0[] = {{{str_u0}}};
double u1[] = {{{str_u1}}};

double p0[] = {{{str_p0}}};
double p1[] = {{{str_p1}}};

double c = {str(self.c)};

void setup() {{
    Serial.begin(9600);

}}

void loop() {{
    //Data Section: To Be Coded Manually

    float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

    //ML Inference Section

    double term1 = 0.0;
    double term2 = 0.0;

    for(int i=0; i<{str(self.dim)}; i++)
    {{
        term1 += p0[i] * (data[i] - u0[i]) * (data[i] - u0[i]);
        term2 += p1[i] * (data[i] - u1[i]) * (data[i] - u1[i]);
    }}

    double temp = term1 - term2;

    if(temp >= c)
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

    



