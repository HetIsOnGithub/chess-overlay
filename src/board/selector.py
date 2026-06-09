import cv2


class BoardSelector:

    def select_region(self, image):

        region = cv2.selectROI(
            "Select Chess Board",
            image,
            showCrosshair=True,
            fromCenter=False
        )

        cv2.destroyAllWindows()

        x, y, w, h = region

        return {
            "left": int(x),
            "top": int(y),
            "width": int(w),
            "height": int(h)
        }