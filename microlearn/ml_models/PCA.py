import math
import numpy as np 

class OffloadPCA:
    def __init__(self, model, scaler):
        self.scaler = scaler
        self.n_components = model.n_components_
        self.mean_vector = model.mean_
        self.pca_components = model.components_.T 
        self.dim = len(self.mean_vector)
        if scaler:
            self.u = scaler.mean_
            self.p = np.reciprocal(scaler.scale_)

    def get_params(self):
        return {'Number_PCA_Components':self.n_components, 'Mean_Vector':self.mean_vector, 'PCA_Components':self.pca_components}

    def get_pca_params_string(self):
        pca_components_terms = []
        for term in self.pca_components:
            temp = '{' +  ', '.join([str(x) for x in term]) + '}'
            pca_components_terms.append(temp)
        str_pca_components = ', '.join(pca_components_terms)
        str_mean_vector = ', '.join([str(x) for x in self.mean_vector])
        return str_pca_components, str_mean_vector

    def get_scaling_params_string(self):
        str_u = ', '.join([str(x) for x in self.u])
        str_p = ', '.join([str(x) for x in self.p])
        return str_u, str_p

    def unscaled_pca_arduino_code(self):
        str_pca_components, str_mean_vector = self.get_pca_params_string()

        code = f"""double pca_components[{str(self.dim)}][{str(self.n_components)}] = {{{str_pca_components}}};
double mean_vector[] = {{{str_mean_vector}}};

void setup() {{
    Serial.begin(9600);

}}

void loop() {{
    //Data Section: To Be Coded Manually

    float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

    //ML Inference Section

    for(int i=0; i<{str(self.dim)}; i++)
    {{
        data[i] = data[i] - mean_vector[i]; //Center the feature vector.
    }}

    double data_pca_transformed[{str(self.n_components)}] = {{ 0.0 }}; 
    for(int col=0; col<{str(self.n_components)}; col++)
    {{
        double temp = 0.0;
        for(int i=0; i<{str(self.dim)}; i++)
        {{
            data_pca_transformed[col] += data[i] * pca_components[i][col];
        }}
    }}

    //Do something with the PCA transformed feature vector: data_pca_transformed.
    Serial.println("PCA Transformation Complete");

    delay(1000);
}}"""
        return code


    def scaled_pca_arduino_code(self):
        str_pca_components, str_mean_vector = self.get_pca_params_string()
        str_u, str_p = self.get_scaling_params_string()

        code = f"""double pca_components[{str(self.dim)}][{str(self.n_components)}] = {{{str_pca_components}}};
double mean_vector[] = {{{str_mean_vector}}};
double u[] = {{{str_u}}};
double p[] = {{{str_p}}};

void setup() {{
    Serial.begin(9600);

}}

void loop() {{
    //Data Section: To Be Coded Manually

    float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

    //ML Inference Section

    for(int i=0; i<{str(self.dim)}; i++)
    {{
        data[i] = (((data[i] - u[i]) * p[i]) - mean_vector[i]); //Standard Scaling and Centering.
    }}

    double data_pca_transformed[{str(self.n_components)}] = {{ 0.0 }}; 
    for(int col=0; col<{str(self.n_components)}; col++)
    {{
        double temp = 0.0;
        for(int i=0; i<{str(self.dim)}; i++)
        {{
            data_pca_transformed[col] += data[i] * pca_components[i][col];
        }}
    }}

    //Do something with the PCA transformed feature vector: data_pca_transformed.
    Serial.println("PCA Transformation Complete");

    delay(1000);
}}"""
        return code


    def get_arduino_code(self):
        if self.scaler:
            return self.scaled_pca_arduino_code()
        return self.unscaled_pca_arduino_code()
