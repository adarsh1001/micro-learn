import math
import numpy as np 

class OffloadSVM:
    def __init__(self, model, scaler):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        if model.__repr__().split('(')[0] == 'SVC' and model.__dict__['kernel'] != 'linear':
            raise TypeError("Only linear SVM is supported! Pass kernel = 'linear' to SVC or use LinearSVC.")
        self.w = model.coef_[0]
        self.c = -1*model.intercept_[0]
        self.u = scaler.mean_
        self.p = np.reciprocal(scaler.scale_)
        self.dim = len(self.w)

    def get_params(self):
        return {'Weight_Vector':self.w, 'Negative_Intercept_Constant':self.c, 'Scaler_Mean_Vector': self.u, 'Scaler_Inv_SD_Vector': self.p}

    def get_arduino_code(self):
        str_w = ', '.join([str(x) for x in self.w])
        str_u = ', '.join([str(x) for x in self.u])
        str_p = ', '.join([str(x) for x in self.p])

        code = f"""double w[] = {{{str_w}}};
double u[] = {{{str_u}}};
double p[] = {{{str_p}}};

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
        temp += (data[i]-u[i]) * p[i] * w[i];
    }}

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
