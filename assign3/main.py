# External packages
import click


@click.group()
def cli():
    pass

# Intrinsische Matrix aus EXIF Daten
# Fundamental Matrix erstellen
# Rektifizieren
# Stereo Algos anwenden
# Depth map


@cli.command('depth')
def depth_cmd():
    pass


@cli.command('sweep')
def sweep_cmd():
    pass
