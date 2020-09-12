import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="micro-learn",
    version="0.0.2",
    author="Adarsh Pal Singh",
    author_email="adarshpalsingh1996@gmail.com",
    description="A Python library to export scikit-learn models to microcontrollers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adarsh1001/micro-learn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
