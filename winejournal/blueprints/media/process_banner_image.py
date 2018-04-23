import os
import os.path

from PIL import Image

from config.settings import TEMP_IMAGE_PATH


# The goal here is to create an image 1140px wide when the image is vertical
# and 350px tall when image is horizontal

class ProcessBannerImage():

    def __init__(self, image, rotate=0, max_dimension=1140):
        self.raw_image = os.path.join(TEMP_IMAGE_PATH, image)
        if rotate == '':
            rotate = 0
        self.rotate = int(rotate)
        self.image = Image.open(self.raw_image)
        self.size = (max_dimension, max_dimension)
        self.upper = self.get_crop_upper()
        self.left = self.get_crop_left()
        self.right = self.get_crop_right()
        self.bottom = self.get_crop_bottom()


    def process_image(self):
        box = (self.upper, self.left, self.right, self.bottom)
        if self.rotate > 0:
            rotated_image = self.image.rotate(self.rotate, expand=True)
            rotated_image.thumbnail(self.size, Image.LANCZOS)
            cropped_image = rotated_image.crop(box)
            cropped_image.save(self.raw_image)
        else:
            self.image.thumbnail(self.size, Image.LANCZOS)
            cropped_image = self.image.crop(box)
            cropped_image.save(self.raw_image)

        return self.raw_image

    def get_crop_upper(self):
        return 0

    def get_crop_left(self):
        return 200

    def get_crop_right(self):
        return 1140

    def get_crop_bottom(self):
        return 550
