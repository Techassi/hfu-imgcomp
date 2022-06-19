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

### Extract

This subcommand allows the user to read a MKV video file, which consists of RGBD images (RGB images with depth
information). First the script reads every frame until we reach the end of the file. After that the script splits every
frame into an RGB and depth image and saves them in separate JPG and PNG files.

```shell
python main.py export
python main.py export --path path/to/data/base/path
```

### Reconstruction

After we extracted separate image files, we can use the Open3D reconstruction system. The systems works in four
different steps:

- The first step makes fragments from a pair of RGBD images. This is done in parallel via a multi-threaded task worker.
- The second step takes those fragments and aligns them to each other in global space.
- The third step refines the alignment.
- The forth and last step combines the fragments into a single volume and exports the mesh as a PLY file.

The config used is:

```json
{
    "name": "Open3D reconstruction",
    "path_dataset": "path/to/assign4/.data",
    "path_intrinsic": "path/to/assign4/.data/intrinsics.json",
    "depth_max": 3.0,
    "voxel_size": 0.05,
    "depth_diff_max": 0.07,
    "preference_loop_closure_odometry": 0.1,
    "preference_loop_closure_registration": 5.0,
    "tsdf_cubic_size": 3.0,
    "icp_method": "color",
    "global_registration": "ransac",
    "python_multi_threading": true
}
```

To run the system each steps needs to be executed in the correct order via the following commands:

```shell
cd examples/python/reconstruction_system

python run_system.py --config ./config/tutorial.json --make
python run_system.py --config ./config/tutorial.json --register
python run_system.py --config ./config/tutorial.json --refine
python run_system.py --config ./config/tutorial.json --integrate
```

The resulting mesh can be opened with MeshLab or other 3D mesh viewers.

**Note:** There was a bug in the reconstruction system code on the master branch. The bug fix was applied locally but
a [PR](5219) was opened to fix it.

## References

- [http://www.open3d.org/docs/release/tutorial/reconstruction_system/system_overview.html](http://www.open3d.org/docs/release/tutorial/reconstruction_system/system_overview.html)
- [http://www.open3d.org/docs/release/python_api/open3d.io.AzureKinectMKVReader.html](http://www.open3d.org/docs/release/python_api/open3d.io.AzureKinectMKVReader.html)
- [http://www.open3d.org/docs/release/python_api/open3d.geometry.RGBDImage.html](http://www.open3d.org/docs/release/python_api/open3d.geometry.RGBDImage.html)

**Disclaimer**

Only the extraction code is written by us. The reconstruction system used can be found
[here](https://github.com/isl-org/Open3D/tree/master/examples/python/reconstruction_system).