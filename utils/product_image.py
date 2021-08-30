from django.core.files.images import File
from django.conf import settings

from io import BytesIO
from PIL import Image
import os


LANCZOS = Image.LANCZOS

def resize(image, size, resample=LANCZOS):
    resize = ResizeProductImages(image, size, resample)
    img = resize.setup_resize()
    return img

class ResizeProductImages:
    def __init__(self, image, size, resample=LANCZOS):
        self.image = image
        self.size = size
        self.resample = resample

        self.image_fp = self.get_image_fp
        self.new_image_name = self.get_new_image_name

    @property
    def get_image_fp(self):
        return os.path.join(settings.MEDIA_ROOT, self.image.name)

    @property
    def get_new_image_name(self):
        basename = os.path.splitext(os.path.basename(self.image_fp))[0]
        return f"{basename}_Cmprssd.jpg"
         
    def setup_resize(self):
        image_ext = os.path.splitext(self.image.name)[1]

        if image_ext in ('.jpg', '.jpeg'):
            return self.resize_img(colors='RGB')
        elif image_ext == '.png':
            return self.resize_img(colors='RGBA')
        else:
            return None

    def resize_img(self, colors):
        with Image.open(self.image_fp).convert(colors) as img:
            if colors == 'RGBA':
                white_background = Image.new('RGBA', img.size, (255, 255, 255))

                img = Image.alpha_composite(
                    white_background, img
                ).convert('RGB')
            
            if img.width < self.size[0]:
                self.size = (round(img.width * 0.99), round(img.height * 0.99))
            
            img.thumbnail(self.size, self.resample)

            thumb_io = BytesIO()
            img_file = File(thumb_io, name=self.new_image_name)
            img.save(thumb_io, format='jpeg', quality=85, optimize=True)

        os.remove(self.image_fp)
        return img_file
