# Assignment 2

Implement a script with Python and OpenCV that calculates the height of an object given a reference object placed on the
same plane. Given three exemplary images (images\table_bottle_*.jpg) of a table showing two objects - a bottle and a
mug. The bottle has a height* of 26 cm. Calculate the height of the mug in cm. Write a readme file that explains what
you have done and how to run the script and what the script does.

## Getting started

To install all required dependencies consult [this](../README.md#setup) section. The core dependencies for this
assignment are:

- OpenCV: `opencv-python`. A wrapper package for OpenCV python bindings. OpenCV is a library of programming functions
  mainly aimed at real-time computer vision. ([PyPI](https://pypi.org/project/opencv-python/))
- Numpy: `numpy`. Package for multi-dimensional arrays and matrices and a large collection of math operations on these
  data structures. ([PyPI](https://pypi.org/project/numpy/))
- Click: `click`. Click is a Python package for creating beautiful command line interfaces in a composable way with as
  little code as necessary. ([PyPI](https://pypi.org/project/click/))

All dependencies (which include indirect dependencies) and their exact version numbers can be found in
[requirements.txt](../requirements.txt). After the installation of the dependencies, we `cd` into the `assign2` folder

```shell
cd assign2
```

## Usage

For a quick overview off all commands run

```shell
python main.py --help
```

To retrieve usage information on each subcommand run

```shell
python main.py <COMMAND> --help
```

### Select lines to calculate mug height

This subcommand will search for images in the `.data` folder. The user has the possibility to select one of the found
images to calculate the height of the mug.

```shell
python main.py line
```

It is possible to adjust the source image path via:

```shell
python main.py line -p .data
```