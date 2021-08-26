from django.core.files.images import File
from django.conf import settings

from PIL import Image, ImageOps
from io import BytesIO
import os

from apps.product import models


def resize(image, product):
    """ Shortcut to resize image and create a thumbnail based on it """
    resize = ResizeImagePIL(image, product)
    resize.resize_image_thumbnail()

def resize_thumb(thumbnail):
    """ Shortcute to resize only the thumbnail """
    resize = ResizeImagePIL(thumbnail)
    resize.resize_thumbnail(just_thumbnail=True)

class ResizeImagePIL:
    def __init__(self, image, product=None):
        self.image = image
        self.product = product

        self.image_name = self.image.name
        self.img_fp = os.path.join(settings.MEDIA_ROOT, self.image.name)

    def resize_image_thumbnail(self):
        """ Handles the time of calling each function """
        len_product_img = models.ProductImage.objects.filter(
            product__name=self.product
        ).count()

        self.resize_image()

        if len_product_img != 1:
            return
        
        self.resize_thumbnail()
  
    def resize_image(self):
        """ Handles the resizing of `self.image` """
        with Image.open(self.img_fp) as img_pil:
            LANCZOS = Image.LANCZOS
            new_sizes = (
                round(img_pil.width * 0.85), round(img_pil.height * 0.85)
            )
            resized_img_pil = img_pil.resize(
                size=new_sizes,
                resample=LANCZOS
            )
            resized_img_pil.save(fp=self.img_fp, optimize=True)
            return

    def resize_thumbnail(self, just_thumbnail=False):
        """ Creates and resizes the thumbnail based on the `self.image` """
        NEW_THUMBNAIL_SIZE = (228, 228)
        ANTIALIAS = Image.ANTIALIAS

        with Image.open(self.img_fp) as img_pil:
            if just_thumbnail is False:
                if self.product.thumbnail:
                    return img_pil
                thumbnail = img_pil.copy()
            else:
                thumbnail = img_pil

            # Thumbnail file's modifications
            pad_thumbnail = ImageOps.pad(
                image=thumbnail, size=NEW_THUMBNAIL_SIZE,
                method=ANTIALIAS, color='white',
            )

            if just_thumbnail is True:
                pad_thumbnail.save(self.img_fp, 'png', optimize=True)
                return
            
            thumbnail_io = BytesIO()
            pad_thumbnail.save(thumbnail_io, 'png', optimize=True)
            thumbnail_file = File(thumbnail_io)

            # Saving thumbnail to Product
            self.product.thumbnail = thumbnail_file
            self.product.save()
            return
