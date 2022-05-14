import click

import utils.images as images
import utils.input as inp
import exif.exif as exif


def execute(base_path: str):
    ''''''
    img_paths, ok = images.list(base_path)
    if not ok:
        click.echo('No images found')

    images.print_list(img_paths)

    index = inp.enforce_range_input(
        f'Enter number between 1 and {len(img_paths)} to select image to use: ', 1, len(img_paths))

    m, err = exif.get_intrinsic_matrix(img_paths[index - 1])
    if err != None:
        click.echo(f'Failed to calculate intrinsic matrix: {err.message}')
        return

    print(m)
