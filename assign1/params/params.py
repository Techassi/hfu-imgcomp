import click
import cv2 as cv


def do():
    """Compute the camera parameters"""
    # Create a video capture
    cap = cv.VideoCapture(0)

    # List of parameters
    params = [
        ["Height", cv.CAP_PROP_FRAME_HEIGHT],
        ["Aperture", cv.CAP_PROP_APERTURE],
        ["Width", cv.CAP_PROP_FRAME_WIDTH]
    ]

    click.echo("Camera parameters")
    click.echo("-----------------")

    # Print all paramters defined above
    for p in params:
        click.echo(f"{p[0]}: {cap.get(p[1])}")
