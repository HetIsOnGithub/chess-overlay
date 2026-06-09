import cv2
import numpy as np


class OccupancyDetector:

    def is_occupied(self, square_image):

        gray = cv2.cvtColor(
            square_image,
            cv2.COLOR_BGR2GRAY
        )

        std_dev = np.std(gray)

        return std_dev > 15