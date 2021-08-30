"""
App product's useful functions
"""
from django.core.files.images import File
from django.utils.text import slugify
from django.conf import settings

from io import BytesIO
from PIL import Image
import os


LANCZOS = Image.LANCZOS

def auto_slug(pk:int, name:str):
    """ Create a slug concatenating `name` and `pk` / `id ` """
    dash_id = f'-{pk}'
    return slugify(name) + dash_id

def resize(image:object, size:tuple):
    """ Shortcut to resize images """
    resize = ResizeProductImages(image, size)
    img = resize.setup_resize()
    return img

class ResizeProductImages:
    def __init__(self, image:object, size:tuple, resample=LANCZOS):
        self.image = image
        self.size = size
        self.resample = resample

        self.image_fp = self.get_image_fp
        self.new_image_name = self.get_new_image_name

    @property
    def get_image_fp(self) -> str:
        """ Concatenate project's media folder and the image's name """
        return os.path.join(settings.MEDIA_ROOT, self.image.name)

    @property
    def get_new_image_name(self) -> str:
        """ Get just the name of the image and join it with `_Cmprssd.jpg` """
        basename = os.path.splitext(os.path.basename(self.image_fp))[0]
        return f"{basename}_Cmprssd.jpg"
         
    def setup_resize(self) -> object:
        """ Handle the image color's type and call the `resize_img` """
        img_ext = os.path.splitext(self.image.name)[1] 

        colors = 'RGB' if img_ext in ('.jpg', '.jpeg') else 'RGBA'
        resized_img = self.resize_img(colors)
        return resized_img

    def resize_img(self, colors) -> object:
        """ Resize and optimize the given images """
        with Image.open(self.image_fp).convert(colors) as img:

            # Treat the image before resizing
            if colors == 'RGBA':
                white_background = Image.new('RGBA', img.size, (255, 255, 255))

                img = Image.alpha_composite(
                    white_background, img
                ).convert('RGB')
            
            # Adjusts the size to 99% of the image
            if img.width < self.size[0]:
                self.size = (round(img.width * 0.99), round(img.height * 0.99))
            
            img.thumbnail(self.size, self.resample)

            # Handle the image file saving
            img_io = BytesIO()
            img_file = File(img_io, name=self.new_image_name)
            img.save(img_io, format='jpeg', quality=50, optimize=True)

        os.remove(self.image_fp)
        return img_file
