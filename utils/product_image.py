from django.core.files.images import File
from django.conf import settings

from PIL import Image, ImageOps
from pathlib import Path
from io import BytesIO
import os

from apps.product import models


def resize(image, product):
    """ It takes care of calling the class instance's function """
    resize = ResizeImagePIL(image, product)
    resize.resize_image_thumbnail()
    return resize

class ResizeImagePIL:
    def __init__(self, image, product):
        self.image = image
        self.product = product

    def resize_image_thumbnail(self):
        """ Handles the time of calling each function """
        self.image_name = self.image.name
        self.img_fp = os.path.join(settings.MEDIA_ROOT, self.image.name)

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

    def resize_thumbnail(self):
        """ Creates and resizes the thumbnail based on the `self.image` """
        NEW_THUMBNAIL_SIZE = (228, 228)
        ANTIALIAS = Image.ANTIALIAS

        with Image.open(self.img_fp) as img_pil:
            if self.product.thumbnail:
                return img_pil
            
            # Managing names
            img_pil_name = Path(self.image_name)
            thumb_pil_name = f'{img_pil_name}_thumbnail.png'
            
            # Thumbnail file's modifications 
            thumbnail = img_pil.copy()
            thumbnail = ImageOps.pad(
                image=thumbnail, size=NEW_THUMBNAIL_SIZE,
                method=ANTIALIAS, color='white',
            )
            thumbnail_io = BytesIO()
            thumbnail.save(thumbnail_io, 'png', optimize=True)
            thumbnail_file = File(
                thumbnail_io, name=thumb_pil_name
            )

            # Saving thumbnail to Product
            self.product.thumbnail = thumbnail_file
            self.product.save()
            return
