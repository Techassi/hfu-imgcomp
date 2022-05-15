# External packages
import click

import cmd.features as features
import cmd.rectify as rectify
import cmd.matrix as matrix
import cmd.dmap as dmap

# Intrinsische Matrix aus EXIF Daten
# Fundamental Matrix erstellen
# Rektifizieren
# Stereo Algos anwenden
# Depth map


@click.group()
def cli():
    pass


@cli.group('features')
def features_group():
    '''
    Detect various features in images.
    '''
    pass


@cli.group('map')
def map_group():
    '''
    Compute depth maps.
    '''
    pass


@cli.command('matrix')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
def matrix_cmd(path: str):
    '''
    Calculate the intrinsic camera matrix.
    '''
    matrix.execute(path)


@cli.command('rectify')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
@click.option('--preview', default=False, help='Show preview windows', type=bool, show_default=True, is_flag=True)
def rectify_cmd(path: str, preview: bool):
    '''
    Rectify two or more images.
    '''
    rectify.execute(path, preview)


@features_group.command('lines')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
@click.option('--preview', default=False, help='Show preview windows', type=bool, show_default=True, is_flag=True)
def epilines_cmd(path: str, preview: bool):
    '''
    Extract epipolar lines from two or more images.
    '''
    features.epilines(path, preview)


@features_group.command('points')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
@click.option('--preview', default=False, help='Show preview windows', type=bool, show_default=True, is_flag=True)
def points_cmd(path: str, preview: bool):
    '''
    Extract matching feature points.
    '''
    features.points(path, preview)


@map_group.command('single')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
@click.option('--preview', default=False, help='Show preview windows', type=bool, show_default=True, is_flag=True)
def single_map_cmd(path: str, preview: bool):
    '''
    Compute a single depth map from two images.
    '''
    dmap.single(path, preview)


@map_group.command('multi')
def multi_map_cmd():
    '''
    Combine several depth maps from two images.
    '''
    pass


@cli.command('sweep')
def sweep_cmd():
    pass


if __name__ == '__main__':
    cli()
