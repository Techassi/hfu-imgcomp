import click

import cmd.export as export


@click.group()
def cli():
    pass


@cli.command('view')
@click.option('-p', '--path', default='.data', help='Path to source MKV video', type=str, show_default=True)
def view_cmd(path: str):
    '''
    Reconstruct 3D scene from a video and view it in an interactive 3D viewer
    '''
    pass


@cli.command('export')
@click.option('-p', '--path', default='.data', help='Path to source MKV video', type=str, show_default=True)
def export_cmd(path: str):
    '''
    Reconstruct 3D scene from a video and export it in a PLY file
    '''
    export.execute(path)


if __name__ == '__main__':
    cli()
