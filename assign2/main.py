# External packages
import click

# Local modules
import line.line as line


@click.group()
def cli():
    pass


@click.command("line")
@click.option('-p', '--path', default='.data', help='Path to the source directory')
def line_cmd(path: str):
    '''Compute the vanishing line based on a selected plane'''
    line.do(path)


cli.add_command(line_cmd)

if __name__ == '__main__':
    cli()
