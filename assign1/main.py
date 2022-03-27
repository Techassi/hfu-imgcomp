# External packages
import click

# Local packages
import prettify.prettify as prettify
import capture.capture as capture
import params.params as params
import print.print as print


@click.group()
def cli():
    pass


@click.command('capture')
@click.option('-n', '--count', default=3, help="Number of pictures")
@click.option('-p', '--path', default=".data", help="Path to the data directory")
def capture_cmd(count: int, path: str):
    """Capture a set of images for the calibration process"""
    capture.do(count, path)


@click.command('params')
def params_cmd():
    """Compute the camera parameters"""
    params.do()


@click.command('prettify')
def prettify_cmd():
    """Undistort live image from a camera"""
    prettify.do()


cli.add_command(prettify_cmd)
cli.add_command(capture_cmd)
cli.add_command(params_cmd)

if __name__ == '__main__':
    cli()
