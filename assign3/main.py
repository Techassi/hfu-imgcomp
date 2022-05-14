# External packages
import click

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


@cli.command('depth')
def depth_cmd():
    pass


@cli.command('sweep')
def sweep_cmd():
    pass


if __name__ == '__main__':
    cli()
