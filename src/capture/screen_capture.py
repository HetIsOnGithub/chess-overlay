import mss
import numpy as np
import cv2


class ScreenCapture:

    def capture_fullscreen(self):

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            screenshot = sct.grab(monitor)

            image = np.array(screenshot)

            return cv2.cvtColor(
                image,
                cv2.COLOR_BGRA2BGR
            )

    def capture_region(self, region):

        with mss.mss() as sct:

            screenshot = sct.grab(region)

            image = np.array(screenshot)

            return cv2.cvtColor(
                image,
                cv2.COLOR_BGRA2BGR
            )