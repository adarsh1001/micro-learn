[![PyPI version](https://badge.fury.io/py/micro-learn.svg)](https://badge.fury.io/py/micro-learn)

**Micro-learn** is a Python library for converting machine learning models trained using scikit-learn into inference code that can run on virtually any microcontroller in real time.

Machine learning algorithms typically require heavy computing and memory resources in the training phase, far greater than what a typical constrained microcontroller can offer. However, post training, many of these algorithms boil down to simple parameters that require simple arithmetic and logical operations for inference. These can easily run on microcontrollers in real time. In a nutshell, train your ML models on a resource-abundant machine using scikit-learn and, with a single line of code, export that trained model into C++/Arduino code using micro-learn!

All the inference algorithms are optimized for microcontrollers and require least possible arithmetic computations. For example, division operations have been converted to multiplications since the latter is much more computationally efficient in microcontrollers. Note that all the algorithms are exact and not approximate. Please refer to my [ACM paper](https://dl.acm.org/doi/abs/10.1145/3341105.3373967) for more insights.

## Installation

### Dependencies

- Python (>= 3.6)
- NumPy (>= 1.13.3)

### User Installation
Use Python3 pip to install the latest micro-learn package.

```bash
pip install micro-learn
```

## Supported Algorithms
The following scikit-learn models are supported as of now:

#### Supervised Learning (Classification)
- Perceptron
- Logistic Regression (Logit)
- Gaussian Naive Bayes (GNB)
- Passive-Aggressive Classifier (PA)
- Linear Discriminant Analysis (LDA)
- Quadratic Discriminant Analysis (QDA)
- Support Vector Machine (SVM) (Linear Kernel)

*Note that only binary-class classification is supported as of now. Support for multi-class classification coming soon!*

#### Supervised Learning (Regression)
- Linear Regression (LR)

#### Unsupervised Learning (Clustering)
- KMeans

#### Unsupervised Learning (Dimensionality Reduction)
- Principal Component Analysis (PCA)

*Support for other scikit-learn models coming soon!*

## Usage
Train any of the supported machine learning models using scikit-learn and simply pass this trained model to micro-learn's *Offload()*. Example for *Gaussian Naive Bayes* is shown below. All other supported algorithms follow the exact same sequence except for SVM in which *Offload()* expects a fitted *StandardScaler* model as a second argument since the algorithm is scale variant. 

```python
>>> from sklearn.naive_bayes import GaussianNB
>>> gnb = GaussianNB()
>>> gnb.fit(X, Y)
>>> from microlearn.offloader import Offload
>>> off = Offload(gnb) #Simply pass your trained model!
>>> off.export_to_arduino('/home/adarsh1001/gnb.ino')
```

And that's it! The output Arduino template will have the corresponding ML inference code along with all the trained parameters. After exporting, open the .ino file and edit the data section and the output class label section as per your need. And of course, since the Arduino programming language is a derivative of C/C++, you can directly edit the template and convert it into a generic .c or .cpp code. For a more detailed guide, you can check out my [medium post](https://medium.com/analytics-vidhya/micro-learn-getting-started-with-machine-learning-on-arduino-52167bc34c1d) on this.

## Project History
I started working on embedded machine learning, both from a theoretical as well as practical perspective, in August 2019 as part of my MS. In November 2019, my paper on a related topic was accepted in ACM SAC. The work on coding a unified library for offloading trained ML models to microcontroller code (micro-learn) was started in May 2020.

### Citation
If you use micro-learn in a scientific publication, please do cite my [paper](https://dl.acm.org/doi/abs/10.1145/3341105.3373967).
