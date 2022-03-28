import os
import click
import cv2 as cv


def do(count: int, path: str):
    """Capture a set of images for the calibration process"""
    click.echo(f"Ready to capture {count} images")
    click.echo("Press <C> to capture image")

    # Check if the .data dir exists. If not, create it
    if not os.path.exists(path):
        os.mkdir(path)

    # Create a video capture
    cap = cv.VideoCapture(0)

    # Create a preview window
    cv.namedWindow("preview")

    i = 0
    while i < count:
        # Read current frame from the video capture
        ok, frame = cap.read()
        if not ok:
            break

        # Preview the frame in the named window
        cv.imshow("preview", frame)
        # Needs to wait some seconds in order not to freeze in preview
        code = cv.waitKey(10)

        # Exit if we press q
        if code == ord("q"):
            break

        # Save image to disk when we press c
        if code == ord("c"):
            save_image(i, path, frame)
            click.echo(f" - {count-i-1} remaining")
            i += 1

    # Release the video capture and destroy the named window
    cap.release()
    cv.destroyAllWindows()


def save_image(idx: int, base_path: str, frame) -> bool:
    """Saves a frame as an image"""
    p = os.path.join(base_path, f"img{idx}.jpg")
    ok = cv.imwrite(p, frame)
    if not ok:
        click.echo(f"Failed to save image at {p}")
        return False

    click.echo(f"Captured image at {p}", nl=False)
    return True
