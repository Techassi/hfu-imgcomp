# External packages
import click

# Local packages
import prettify.prettify as prettify
import capture.capture as capture
import params.params as params
import error.error as error


@click.group()
def cli():
    pass


@click.command('capture')
@click.option('-n', '--count', default=3, help='Number of pictures')
@click.option('-p', '--path', default='.data', help='Path to the source directory')
def capture_cmd(count: int, path: str):
    '''Capture a set of images for the calibration process'''
    capture.do(count, path)


@click.command('params')
@click.option('-c', '--camera', default=0, help='Index of camera device')
def params_cmd(camera: int):
    '''Compute the camera parameters'''
    params.do(camera)


@click.command('prettify')
@click.option('-c', '--camera', default=0, help='Index of camera device')
@click.option('-s', '--source', default=".data", help='Path to the source directory')
@click.option('-r', '--results', default='.results', help='Path to the result directory')
@click.option('-l', '--live', default=False, help='Live mode undistorts a live camera stream', is_flag=True)
@click.option('-p', '--preview', default=False, help='Display preview windows for the calibration and result images', is_flag=True)
def prettify_cmd(camera: int, source: str, results: str, live: bool, preview: bool):
    '''Undistort live image from a camera'''
    prettify.do(camera, source, results, live, preview)


@click.command('error')
@click.option('-s', '--source', default=".data", help='Path to the source directory')
@click.option('-p', '--preview', default=False, help='Display preview windows for the calibration images', is_flag=True)
def error_cmd(source: str, preview: bool):
    '''Print the reprojection error'''
    error.do(source, preview)


cli.add_command(prettify_cmd)
cli.add_command(capture_cmd)
cli.add_command(params_cmd)
cli.add_command(error_cmd)

if __name__ == '__main__':
    cli()
