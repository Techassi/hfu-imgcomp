# External packages
import click

import cmd.features as features
import cmd.matrix as matrix


@click.group()
def cli():
    pass

# Intrinsische Matrix aus EXIF Daten
# Fundamental Matrix erstellen
# Rektifizieren
# Stereo Algos anwenden
# Depth map


@cli.command('matrix')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
def matrix_cmd(path: str):
    '''
    Calculate the intrinsic camera matrix.
    '''
    matrix.execute(path)


@cli.command('features')
@click.option('-p', '--path', default='.data', help='Path to source images', type=str, show_default=True)
@click.option('--preview', default=False, help='Show preview windows', type=bool, show_default=True, is_flag=True)
def features_cmd(path: str, preview: bool):
    ''''''
    features.execute(path, preview)


@cli.command('depth')
def depth_cmd():
    pass


@cli.command('sweep')
def sweep_cmd():
    pass


if __name__ == '__main__':
    cli()
