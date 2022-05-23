import click

import features.features as features
import utils.images as images
import utils.input as inp
import exif.exif as exif


def execute(base_path: str, preview: bool):
    ''''''
    imgs, combi_mode, ref_index = inp.handle_images(base_path, preview)
    ic_list = images.get_combinations(imgs, combi_mode, ref_index)

    intrinsic_matrix, err = exif.get_intrinsic_matrix(imgs[0][1])
    if err != None:
        click.echo(f'Failed to calculate intrinsic matrix: {err.message}')
        return

    click.echo('\nExtracting fundamental matrices. This takes a few seconds...')
    fm_list = features.get_fundamental_matrices(imgs, ic_list)
    em_list = features.find_essential_matrices(fm_list, intrinsic_matrix)
