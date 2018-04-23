import os
import os.path

from PIL import Image

from config.settings import TEMP_IMAGE_PATH


# The goal here is to create an image 600px wide when the image is vertical
# and 600px tall when image is horizontal

class ProcessStandardImage():

    def __init__(self, image, rotate=0, max_dimension=600):
        self.raw_image = os.path.join(TEMP_IMAGE_PATH, image)
        if rotate == '':
            rotate = 0
        self.rotate = int(rotate)
        self.image = Image.open(self.raw_image)
        self.size = (max_dimension, max_dimension)

    def process_image(self):

        if self.rotate > 0:
            rotated_image = self.image.rotate(self.rotate, expand=True)
            rotated_image.thumbnail(self.size, Image.LANCZOS)
            rotated_image.save(self.raw_image)
        else:
            self.image.thumbnail(self.size, Image.LANCZOS)
            self.image.save(self.raw_image)

        return self.raw_image
