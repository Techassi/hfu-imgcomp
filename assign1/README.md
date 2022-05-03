# Assignment 1

The task of the first assignment was to write multiple scripts for camera calibration using OpenCV and chessboard
reference images.

## Getting started

To install all required dependencies consult [this](../README.md#setup) section.

All dependencies (which include indirect dependencies) and their exact version numbers can be found in
[requirements.txt](../requirements.txt). After the installation of the dependencies, we `cd` into the `assign1` folder

```shell
cd assign1
```

## Usage

For a quick overview of all commands run

```shell
python main.py --help
```

To retrieve usage information on each subcommand run

```shell
python main.py <COMMAND> --help
```

### Capture images for calibration

> Write a script that allows capturing a set of images for the calibration.

```shell
python main.py capture
```

This subcommand will capture `3` images (default) and will save it into the `.data` folder (default). Each image will be
named `img<INDEX>.jpg`.

It is possible to adjust the number of images to capture and the folder to save the images in:

```shell
python main.py capture --count 10 --path .data
# or
python main.py capture -n 10 -p .data
```

### Camera parameters

> Write a script that computes the camera parameters.

```shell
python main.py params
```

This subcommand will print a selected set of parameters of camera `0` (default). To adjust which camera to use we can
provide an optional option:

```shell
python main.py params --camera 1
# or
python main.py params -c 1
```

### Prettify image(s)

> Write a script that undistorts the live image from a camera.

```shell
python main.py prettify
```

This subcommand can prettify / undistort images either in standalone or live mode. The options are:

```shell
# Adjust source image folder
python main.py prettify --source .data
python main.py prettify -s .data

# Adjust result image folder
python main.py prettify --results .results
python main.py prettify -r .results

# Enable preview windows (for standalone mode)
python main.py prettify --preview
python main.py prettify -p

# Use live mode
python main.py prettify --live
python main.py prettify -l
```

### Reprojection Error

> BONUS: Write a script that computes the reprojection error for one image in mm, including a explanatory output and
> documentation how to use it.

To print the reprojection error based on the calibration images we can use

```shell
python main.py error
```