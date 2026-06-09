import os
import cv2


class PieceDetector:

    def __init__(self):

        self.templates = {}

        self.load_templates()

    def load_templates(self):

        template_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "assets",
                "pieces"
            )
        )

        for filename in os.listdir(
            template_dir
        ):

            if not filename.endswith(".png"):
                continue

            path = os.path.join(
                template_dir,
                filename
            )

            image = cv2.imread(path)

            key = filename.replace(
                ".png",
                ""
            )

            self.templates[key] = image

    def detect_piece(
        self,
        square_image
    ):

        best_score = -1
        best_name = None
        
        h, w = square_image.shape[:2]

        crop = square_image[
        int(h * 0.25):int(h * 0.75),
        int(w * 0.25):int(w * 0.75)
        ]

        for name, template in self.templates.items():

            resized = cv2.resize(
                square_image,
                (
                    template.shape[1],
                    template.shape[0]
                )
            )

            result = cv2.matchTemplate(
                resized,
                template,
                cv2.TM_CCOEFF_NORMED
            )

            score = result[0][0]

            if score > best_score:

                best_score = score
                best_name = name

        if best_name in (
        "empty_light",
        "empty_dark"
    ):
            return None, best_score

        if best_score < 0.55:
            return None, best_score

        return best_name, best_score