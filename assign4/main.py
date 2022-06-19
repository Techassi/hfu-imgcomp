import click

import cmd.extract as extract


@click.group()
def cli():
    pass


@cli.command('extract')
@click.option('-p', '--path', default='.data', help='Path to source MKV video', type=str, show_default=True)
@click.option('-c', '--config', default='.data/config.toml', help="Path to TOML config file", type=str, show_default=True)
def extract_cmd(path: str, config: str):
    '''
    Extract color + depth images from a video and save them in seperate .jpg and .png files
    '''
    extract.execute(path, config)


if __name__ == '__main__':
    cli()
