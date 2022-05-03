# HFU ImgComp

This repository contains source code for all assignments from the lecture **Image processing and computer graphics**.
The source code for each assignment is split upp into separate folders with the naming scheme `assign<NUMBER>`.

## Setup

To setup the work environment and start developing code run the following commands:

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The core dependencies are:

- OpenCV: `opencv-python`. A wrapper package for OpenCV python bindings. OpenCV is a library of programming functions
  mainly aimed at real-time computer vision. ([PyPI](https://pypi.org/project/opencv-python/))
- Numpy: `numpy`. Package for multi-dimensional arrays and matrices and a large collection of math operations on these
  data structures. ([PyPI](https://pypi.org/project/numpy/))
- Click: `click`. Click is a Python package for creating beautiful command line interfaces in a composable way with as
  little code as necessary. ([PyPI](https://pypi.org/project/click/))