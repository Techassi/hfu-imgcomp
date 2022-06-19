import click

import cmd.extract as extract


@click.group()
def cli():
    pass


@cli.command('extract')
@click.option('-p', '--path', default='.data', help='Base data path', type=str, show_default=True)
def extract_cmd(path: str):
    '''
    Extract color + depth images from a video and save them in seperate files
    '''
    extract.execute(path)


if __name__ == '__main__':
    cli()
