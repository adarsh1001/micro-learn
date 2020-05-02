# micro-learn
micro-learn is a Python module for converting trained machine learning models into inference code that can run on microcontrollers in real time.

Machine learning algorithms typically require heavy computing and memory resources in the training phase, far greater than what a typical constrained microcontroller can offer. However, post training, many of these algorithms boil down to simple parameters that require simple arithmetic operations for inference. These can easily run on microcontrollers in real time. The purpose of this library is to convert ML models (trained using scikit-learn) to C/C++/Arduino code.

Please refer to my ACM paper for theoretical and practical foundations regarding this procedure:
https://dl.acm.org/doi/abs/10.1145/3341105.3373967
 
