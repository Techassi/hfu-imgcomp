import click


def do(count: int):
    """Capture a set of images for the calibration process"""
    click.echo(f"Capture {count} images")
