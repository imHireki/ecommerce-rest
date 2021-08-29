from django.core.files.images import File
from django.conf import settings

from io import BytesIO
from PIL import Image
import os

from apps.product import models


SIZE = (256, 256)
LANCZOS = Image.LANCZOS

"""
TODO: add resize manager
TODO: remove unecessary var assignment
TODO: add resize image
TODO: project pattern
    - Resize
        - bind_right_resize
        - resize_image
        - resize_png
        - resize_jpg
"""

def manage_resize(image):
    image_ext = os.path.splitext(image.name)[1]

    if image_ext == '.jpg':
        return resize_jpg(image)
    elif image_ext == '.png': 
        return resize_small_png(image)

    else: return image_ext

def resize_small_png(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f"{os.path.splitext(os.path.basename(thumb_fp))[0]}_Cmprssd.jpg"       
    
    with Image.open(thumb_fp).convert('RGBA') as img:
        size_99 = (round(img.width * 0.99), round(img.height * 0.99))

        bg = Image.new('RGBA', img.size, (255, 255, 255))
        img_comp = Image.alpha_composite(bg, img).convert('RGB')

        img_comp.thumbnail(size_99, LANCZOS)
        
        thumb_io = BytesIO()
        img_file = File(thumb_io, name=new_name)
        img_comp.save(thumb_io, format='jpeg', quality=75, optimize=True)

    os.remove(thumb_fp)
    return img_file

def resize_png(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f"{os.path.splitext(os.path.basename(thumb_fp))[0]}_Cmprssd.jpg"       
    
    with Image.open(thumb_fp).convert('RGBA') as img:
        
        bg = Image.new('RGBA', img.size, (255,255,255))
        img_comp = Image.alpha_composite(bg, img).convert('RGB')

        img_comp.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_name)
        img_comp.save(thumb_io, format='jpeg', quality=75, optimize=True)

    os.remove(thumb_fp)
    return thumbnail

def resize_jpg(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f"{os.path.splitext(os.path.basename(thumb_fp))[0]}_Cmprssd.jpg"       

    with Image.open(thumb_fp).convert('RGB') as img:

        img.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_name)
        img.save(thumb_io, format='jpeg', quality=75, optimize=True)
    
    os.remove(thumb_fp)
    return thumbnail

def resize_small_jpg(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f"{os.path.splitext(os.path.basename(thumb_fp))[0]}_Cmprssd.jpg"       

    with Image.open(thumb_fp).convert('RGB') as img:
        size_99 = (round(img.width * 0.99), round(img.height * 0.99))
        img.thumbnail(size_99, LANCZOS)

        thumb_io = BytesIO()
        img_file = File(thumb_io, name=new_name)
        img.save(thumb_io, format='jpeg', quality=75, optimize=True)
    
    os.remove(thumb_fp)
    return img_file

def resize_image(thumbnail):
    """
    TODO: Send new SIZES to the resize
    """
    ...