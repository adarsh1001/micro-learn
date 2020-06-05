import math
import numpy as np 

class OffloadLogR:
    def __init__(self, model):
        self.class0 = model.__dict__['classes_'][0]
        self.class1 = model.__dict__['classes_'][1]
        self.w = model.coef_[0]
        self.b = model.intercept_[0]
        self.dim = len(self.w)
    
    def get_params(self):
        return {'Weight_Vector':self.w, 'Bias_Constant':self.b}

    def get_arduino_code(self):
        str_w = ', '.join([str(x) for x in self.w])

        code = f"""#include <math.h>
        
double w[] = {{{str_w}}};
double b = {str(self.b)};

double sigmoid(double x)
{{
    return (1 / (1 + exp((-1) * x)));        
}}

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

    if(round(sigmoid(temp + b)) == 1)
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