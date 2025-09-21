# imbalanced-learn

[![GitHub Actions](https://github.com/scikit-learn-contrib/imbalanced-learn/actions/workflows/tests.yml/badge.svg)](https://github.com/scikit-learn-contrib/imbalanced-learn/actions/workflows/tests.yml) [![Codecov](https://codecov.io/gh/scikit-learn-contrib/imbalanced-learn/branch/master/graph/badge.svg)](https://codecov.io/gh/scikit-learn-contrib/imbalanced-learn) [![CircleCI](https://circleci.com/gh/scikit-learn-contrib/imbalanced-learn.svg?style=shield)](https://circleci.com/gh/scikit-learn-contrib/imbalanced-learn/tree/master) [![Python Version](https://img.shields.io/pypi/pyversions/imbalanced-learn.svg)](https://img.shields.io/pypi/pyversions/imbalanced-learn.svg) [![PyPI](https://badge.fury.io/py/imbalanced-learn.svg)](https://badge.fury.io/py/imbalanced-learn) [![Gitter](https://badges.gitter.im/scikit-learn-contrib/imbalanced-learn.svg)](https://gitter.im/scikit-learn-contrib/imbalanced-learn?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

imbalanced-learn is a python package offering a number of re-sampling techniques commonly used in datasets showing strong between-class imbalance. It is compatible with [scikit-learn](http://scikit-learn.org/stable/) and is part of [scikit-learn-contrib](https://github.com/scikit-learn-contrib) projects.

## Documentation

Installation documentation, API documentation, and examples can be found on the [documentation](https://imbalanced-learn.org/stable/).

## Installation

### Dependencies

`imbalanced-learn` requires the following dependencies:

- Python (>= 3.10)
- NumPy (>= 1.25.2)
- SciPy (>= 1.11.4)
- Scikit-learn (>= 1.4.2)
- Pytest (>= 7.2.2)

Additionally, `imbalanced-learn` requires the following optional dependencies:

- Pandas (>= 2.0.3) for dealing with dataframes
- Tensorflow (>= 2.16.1) for dealing with TensorFlow models
- Keras (>= 3.3.3) for dealing with Keras models

The examples will requires the following additional dependencies:

- Matplotlib (>= 3.7.3)
- Seaborn (>= 0.12.2)

### Installation

#### From PyPi or conda-forge repositories

imbalanced-learn is currently available on the PyPi's repositories and you can install it via `pip`:

```bash
pip install -U imbalanced-learn
```

The package is release also in Anaconda Cloud platform:

```bash
conda install -c conda-forge imbalanced-learn
```

#### From source available on GitHub

If you prefer, you can clone it and run the setup.py file. Use the following commands to get a copy from Github and install all dependencies:

```bash
git clone https://github.com/scikit-learn-contrib/imbalanced-learn.git
cd imbalanced-learn
pip install .
```

Be aware that you can install in developer mode with:

```bash
pip install --no-build-isolation --editable .
```

If you wish to make pull-requests on GitHub, we advise you to install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

### Testing

After installation, you can use `pytest` to run the test suite:

```bash
make coverage
```

## Development

The development of this scikit-learn-contrib is in line with the one of the scikit-learn community. Therefore, you can refer to their [Development Guide](http://scikit-learn.org/stable/developers).

## Endorsement of the Scientific Python Specification

We endorse good practices from the Scientific Python Ecosystem Coordination (SPEC). The full list of recommendations is available [here](https://scientific-python.org/specs/).

See below the list of recommendations that we endorse for the imbalanced-learn project.

[![SPEC 0 — Minimum Supported Dependencies](https://img.shields.io/badge/SPEC-0-green?labelColor=%23004811&color=%235CA038)](https://scientific-python.org/specs/spec-0000/)

## About

If you use imbalanced-learn in a scientific publication, we would appreciate citations to the following paper:

```bibtex
@article{JMLR:v18:16-365,
author  = {Guillaume  Lema{{\^i}}tre and Fernando Nogueira and Christos K. Aridas},
title   = {Imbalanced-learn: A Python Toolbox to Tackle the Curse of Imbalanced Datasets in Machine Learning},
journal = {Journal of Machine Learning Research},
year    = {2017},
volume  = {18},
number  = {17},
pages   = {1-5},
url     = {http://jmlr.org/papers/v18/16-365}
}
```

Most classification algorithms will only perform optimally when the number of samples of each class is roughly the same. Highly skewed datasets, where the minority is heavily outnumbered by one or more classes, have proven to be a challenge while at the same time becoming more and more common.

One way of addressing this issue is by re-sampling the dataset as to offset this imbalance with the hope of arriving at a more robust and fair decision boundary than you would otherwise.

You can refer to the [imbalanced-learn](https://imbalanced-learn.org/stable/user_guide.html) documentation to find details about the implemented algorithms.