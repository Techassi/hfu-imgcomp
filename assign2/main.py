# External packages
import click

# Local modules
import edges.edges as edges
import line.line as line
import calc.calc as calc


@click.group()
def cli():
    pass


@click.command('line')
@click.option('-p', '--path', default='.data', help='Path to the source image directory', type=str)
def line_cmd(path: str):
    '''Compute the vanishing line based on a selected plane'''
    line.do(path)


@click.command('calc')
def calc_cmd():
    '''Calculate the height of the mug'''
    calc.do()


@click.command('edges')
@click.option('-p', '--path', default='.data', help='Path to the source image directory', type=str)
@click.option('-u', '--max', default=200, help='Max value for hysteresis thresholding', type=int)
@click.option('-l', '--min', default=100, help='Min value for hysteresis thresholding', type=int)
def edges_cmd(path: str, max: int, min: int):
    '''Automatic edge detection to calculate the vanishing line'''
    edges.do(path, max, min)


cli.add_command(edges_cmd)
cli.add_command(line_cmd)
cli.add_command(calc_cmd)

if __name__ == '__main__':
    cli()
