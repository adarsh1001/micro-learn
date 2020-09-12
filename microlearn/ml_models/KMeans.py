import numpy as np

class OffloadKMeans:
    def __init__(self, model):
        self.num_clusters = model.n_clusters
        self.cluster_centers = model.cluster_centers_
        self.dim = len(self.cluster_centers[0])
    
    def get_params(self):
        return {'Num_Clusters':self.num_clusters, 'Cluster_Centers':self.cluster_centers}

    def get_arduino_code(self):
        cc_terms = []
        for term in self.cluster_centers:
            temp = '{' +  ', '.join([str(x) for x in term]) + '}'
            cc_terms.append(temp)
        str_cc = ', '.join(cc_terms)

        code = f"""double CC[{str(self.num_clusters)}][{str(self.dim)}] = {{{str_cc}}};

double euclidean_sq(float A[], double B[])
{{
    double dist = 0.0;
    for(int i=0; i<{str(self.dim)}; i++)
    {{
        double temp = A[i]-B[i];
        dist += temp*temp;
    }}
    return dist;
}}

void setup() {{
    Serial.begin(9600);

}}

void loop() {{
    //Data Section: To Be Coded Manually

    float data[{str(self.dim)}]; //This is your feature vector. Retrive your data into this array.

    //ML Inference Section

    double min_dist = euclidean_sq(data, CC[0]);
    int label = 0;
    for(int i=1; i<{str(self.num_clusters)}; i++)
    {{
        double temp = euclidean_sq(data, CC[i]);
        if(temp < min_dist)
        {{
            min_dist = temp;
            label = i;
        }}
    }}

    //Do something with the cluster label prediction.
    Serial.println(label);

    delay(1000);
}}"""
        return code
