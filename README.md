# micro-learn
micro-learn is a Python module for converting trained machine learning models into inference code that can run on microcontrollers in real time.

Machine learning algorithms typically require heavy computing and memory resources in the training phase, far greater than what a typical constrained microcontroller can offer. However, post training, many of these algorithms boil down to simple parameters that require simple arithmetic and logical operations for inference. These can easily run on microcontrollers in real time. The purpose of this library is to convert ML models (trained using scikit-learn) directly into Arduino inference code.

All the inference algorithms are optimized for microcontrollers and require least possible arithmetic computations. Division operations have been converted to multiplications since the latter is much more computationally efficient. Note that all the algorithms are exact and not approximate. Please refer to my [ACM paper](https://dl.acm.org/doi/abs/10.1145/3341105.3373967) for theoretical and practical foundations regarding this procedure.

## Installation

### Dependencies

- Python (>= 3.6)
- NumPy (>= 1.13.3)

Tested only on Linux for now.

### User Installation
Pip installable version coming soon! For now, you can clone this repo and directly import the Python packages.

```bash
git clone https://github.com/adarsh1001/micro-learn.git
```

## Supported Algorithms
The following scikit-learn models are supported for now:

- Perceptron
- Linear Regression (LR)
- Gaussian Naive Bayes (GNB)
- Logistic Regression (Logit)
- Linear Discriminant Analysis (LDA)
- Quadratic Discriminant Analysis (QDA)
- Support Vector Machine (SVM) (Linear Kernel)

Note that only binary-class classification models are supported as of now. Support for multi-class and other scikit-learn models coming soon!

## Usage
Train a binary classifier using any of the supported scikit-learn models and simply pass this trained model to Offload(). Example for LDA is shown below. For SVM (LinearSVM or SVC), Offload() expects a fitted StandardScaler model as a second argument since SVM is a scale-variant algorithm. 

```python
>>> from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
>>> lda = LinearDiscriminantAnalysis(store_covariance=True)
>>> lda.fit(X, Y)
>>> from microlearn.offloader import Offload
>>> off = Offload(lda) #Simply pass your trained model!
>>> off.export_to_arduino('/home/adarsh1001/lda.ino')
```

And that's it! The output Arduino template will have the corresponding ML inference code along with all the trained parameters. After exporting, open the .ino file and edit the data section as per your need. And of course, since the Arduino programming language is a derivative of C/C++, you can directly edit the template and convert it into a generic .c or .cpp code. For a more detailed guide, you can check out my [medium post](https://medium.com/analytics-vidhya/micro-learn-getting-started-with-machine-learning-on-arduino-52167bc34c1d) on this.

## Project History
I started working on embedded machine learning, both from a theoretical as well as practical perspective, in August 2019 as part of my MS. In November 2019, my paper on a related topic was accepted in ACM SAC. The work on coding a unified library for offloading trained ML models to microcontroller code (micro-learn) was started in May 2020.

### Citation
If you use micro-learn in a scientific publication, please do cite my [paper](https://dl.acm.org/doi/abs/10.1145/3341105.3373967).
