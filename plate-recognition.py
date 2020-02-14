#!/usr/bin/env python3

import sys
import uuid
from time import sleep
from typing import List

from openalpr import Alpr
from picamera import PiCamera

# TODO: replace writing to a file with writing to an in memory bytearray/numpy array

ALPR = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")

if not ALPR.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)


def take_picture() -> str:
    file_path = f"/tmp/{uuid.uuid4()}.jpg"

    with PiCamera() as camera:
        camera.start_preview()
        sleep(3)  # Give time to focus
        camera.capture(file_path)
        camera.stop_preview()

    return file_path


def recognise_plates(file_path: str) -> List[str]:
    results = ALPR.recognize_file(file_path)

    return results["results"]


def main():
    file_path = take_picture()
    plates = recognise_plates(file_path)

    print(plates)


if __name__ == "__main__":
    main()
