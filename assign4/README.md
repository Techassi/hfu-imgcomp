# Assignment 4

mplement and run a script with Python and Open3D that computes a 3D mesh from an Azure Kinect recording. The input is
only the recording as a .mkv file and the output is one 3D mesh (as .ply file). You can use all example and tutorial
code snippets from the Open3D documentation. Write a readme file that explains:

- how to get from a .mkv file to a 3D mesh,
- how to run the script
- and what the script does.

## Getting started

To install all required dependencies consult [this](../README.md#setup) section.

All dependencies (which include indirect dependencies) and their exact version numbers can be found in
[requirements.txt](../requirements.txt). After the installation of the dependencies, we `cd` into the `assign4` folder

```shell
cd assign4
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

### Export

This subcommand allows the user to reconstruct a 3D scene from a MKV video file. The scene then gets exported as a 3D
mesh (PLY file). In detail the command works like this:

1. Glob the `.data` dir for `.mkv` video files and dislay them in the terminal. The user then can choose which file to
   use for reconstruction. This file then gets read by the Open3D AzureKinectMKVReader, which allows us to iterate over
   each individual frame.
2. Each frame gets fed to the reconstruction system / pipeline. This pipeline consists of multiple steps:
   1. [Make fragments](http://www.open3d.org/docs/release/tutorial/reconstruction_system/make_fragments.html#reconstruction-system-make-fragments):
      build local geometric surfaces (referred to as fragments) from short subsequences of the input RGBD sequence. This
      part uses RGBD Odometry, Multiway registration, and RGBD integration.

```shell
python main.py export
python main.py export --path path/to/mkv/video/file
```

## References

- [http://www.open3d.org/docs/release/tutorial/reconstruction_system/system_overview.html](http://www.open3d.org/docs/release/tutorial/reconstruction_system/system_overview.html)
- [http://www.open3d.org/docs/release/python_api/open3d.io.AzureKinectMKVReader.html](http://www.open3d.org/docs/release/python_api/open3d.io.AzureKinectMKVReader.html)
- [http://www.open3d.org/docs/release/python_api/open3d.geometry.RGBDImage.html](http://www.open3d.org/docs/release/python_api/open3d.geometry.RGBDImage.html)

**Disclaimer** Most of the code is copied directly from the Open3D examples, see:

- [https://github.com/isl-org/Open3D/blob/master/examples/python/reconstruction_system/opencv_pose_estimation.py](https://github.com/isl-org/Open3D/blob/master/examples/python/reconstruction_system/opencv_pose_estimation.py)
- [https://github.com/isl-org/Open3D/blob/master/examples/python/reconstruction_system/make_fragments.py](https://github.com/isl-org/Open3D/blob/master/examples/python/reconstruction_system/make_fragments.py)