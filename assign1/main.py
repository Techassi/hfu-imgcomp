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
@click.option('-n', '--count', default=3, help='Number of pictures')
@click.option('-s', '--source', default='.data', help='Path to the source directory')
def capture_cmd(count: int, path: str):
    '''Capture a set of images for the calibration process'''
    capture.do(count, path)


@click.command('params')
def params_cmd():
    '''Compute the camera parameters'''
    params.do()


@click.command('prettify')
@click.option('-s', '--source', default=".data", help='Path to the source directory')
@click.option('-r', '--results', default='.results', help='Path to the result directory')
@click.option('-p', '--preview', default=False, help='Display preview windows for the calibration and result images', is_flag=True)
def prettify_cmd(source: str, results: str, preview: bool):
    '''Undistort live image from a camera'''
    prettify.do(source, results, preview)


cli.add_command(prettify_cmd)
cli.add_command(capture_cmd)
cli.add_command(params_cmd)

if __name__ == '__main__':
    cli()
