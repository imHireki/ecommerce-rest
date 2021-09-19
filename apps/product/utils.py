"""
App product's useful functions
"""
from django.core.files.images import ImageFile, File
from django.utils.text import slugify
from django.conf import settings

from io import BytesIO
from PIL import Image
import os


LANCZOS = Image.LANCZOS

def auto_slug(pk:int, name:str) -> str:
    """ Create a slug concatenating `name` and `pk` / `id ` """
    dash_id = f'-{pk}'
    return slugify(name) + dash_id

def resize(image:object, size:tuple) -> object:
    """ Shortcut to resize images """
    resize = ResizeProductImages(image, size)
    img = resize.setup_resize()
    return img

def save_img(size:tuple, form:str, color='RGB'):
    """ Manage the image saving """
    img = Image.new(color, size)
    img.save(f'media/tests/{size}_{form}_{color}.{form}', form)
    img.close()

def create_img():
    """ Manage the creation of the test images """
    sizes = ((100, 50), (256, 256), (1280, 720))
    formats = ('png', 'jpeg')
    colors = ('RGBA', 'RGB')

    for s in range(len(sizes)):
        for f in range(len(formats)):
            if formats[f] == 'png':
                for c in range(len(colors)):
                    save_img(sizes[s], formats[f], colors[c])
            else:
                save_img(sizes[s], formats[f])

def get_img_file(name:str, form:str) -> object:
    """ Get the files from the testdir when they're requested """
    with Image.open(f'media/tests/{name}') as image:
        img_io = BytesIO()
        image.save(img_io, format=form)
        image_file = ImageFile(img_io, name=name)
    return image_file


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
