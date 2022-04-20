# External packages
import click

# Local modules
import edges.edges as edges
import line.line as line
import calc.calc as calc


@click.group()
def cli():
    pass


@click.command("line")
@click.option('-p', '--path', default='.data', help='Path to the source directory')
def line_cmd(path: str):
    '''Compute the vanishing line based on a selected plane'''
    line.do(path)


def calc_cmd():
    '''Calculate the height of the mug'''
    calc.do()


def edges_cmd():
    '''Automatic edge detection to calculate the vanishing line'''
    edges.do()


cli.add_command(edges_cmd)
cli.add_command(line_cmd)
cli.add_command(calc_cmd)

if __name__ == '__main__':
    cli()
