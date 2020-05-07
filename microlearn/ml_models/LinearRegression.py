import math 
import numpy as np 

class OffloadLR:
    def __init__(self, model):
        self.w = model.coef_
        self.c = model.intercept_
        self.dim = len(self.w)

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

    double prediction = 0.0;
    for(int i=0; i<{str(self.dim)}; i++)
    {{
        prediction += data[i]*w[i];
    }}
    prediction += c;

    //Do something with the prediction.
    Serial.println(prediction);

    delay(1000);
}}"""
        return code