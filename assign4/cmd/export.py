import open3d as o3d
import click

import utils.input as inp


def execute(base_path: str):
    # Set verbosity level to only errors
    o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

    # Handle MKV video file selection and reading
    images, err = inp.handle_mkv_files(base_path)
    if err != None:
        click.echo(err)
        return
