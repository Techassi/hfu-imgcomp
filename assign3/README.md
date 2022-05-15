# Assignment 3

Implement a script with Python and OpenCV that computes a depth map from at least three images. Write a readme file that
explains what you have done and how to run the script and what the script does.

## Getting started

To install all required dependencies consult [this](../README.md#setup) section.

All dependencies (which include indirect dependencies) and their exact version numbers can be found in
[requirements.txt](../requirements.txt). After the installation of the dependencies, we `cd` into the `assign2` folder

```shell
cd assign3
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

### Intrinsic camera matrix

This subcommand calculates the intrinsic camera matrix based on known values and EXIF data present in the source image:

```shell
python main.py matrix
# or
python main.py matrix -p .data
```

### Rectification

This subcommand rectifies two or more images and displays the result in a window:

```shell
python main.py rectify
# or
python main.py rectify -p .data
# or
python main.py rectify-p .data --preview
```

### Feature extraction

This subcommand extracts epilines from multiple images and displays the result in a window:

```shell
python main.py features lines
# or
python main.py features lines -p .data
# or
python main.py features lines -p .data --preview
```

This subcommand extracts matching points from multiple images and displays the result in a window:

```shell
python main.py features points
# or
python main.py features points -p .data
# or
python main.py features points -p .data --preview
```

## References

- [https://docs.opencv2.org/4.5.5/da/de9/tutorial_py_epipolar_geometry.html](https://docs.opencv2.org/4.5.5/da/de9/tutorial_py_epipolar_geometry.html)
- [https://www.andreasjakl.com/understand-and-apply-stereo-rectification-for-depth-maps-part-2/](https://www.andreasjakl.com/understand-and-apply-stereo-rectification-for-depth-maps-part-2/)
- [https://stackoverflow.com/questions/36172913/opencv-depth-map-from-uncalibrated-stereo-system](https://stackoverflow.com/questions/36172913/opencv-depth-map-from-uncalibrated-stereo-system)
- [https://github.com/uhahne/BildComp-SoSe2022](https://github.com/uhahne/BildComp-SoSe2022)