from django.core.files.images import File
from django.conf import settings

from io import BytesIO
from sys import stdout
from PIL import Image
import os

from apps.product import models


SIZE = (256, 256)
LANCZOS = Image.LANCZOS

def resize_jpg(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = os.path.basename(thumb_fp)

    with Image.open(thumb_fp).convert('RGB') as img:

        img.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_name)
        img.save(
            thumb_io, format='jpeg', quality=75, optimize=True
        )
    
    os.remove(thumb_fp)
    return thumbnail
    

def resize_png(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f'{os.path.splitext(os.path.basename(thumb_fp))[0]}.jpg'
    
    with Image.open(thumb_fp).convert('RGBA') as img:
        
        bg = Image.new('RGBA', img.size, (255,255,255))
        img_comp = Image.alpha_composite(bg, img).convert('RGB')

        img_comp.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_name)
        img_comp.save(
            thumb_io, format='jpeg', quality=75, optimize=True
        )

    os.remove(thumb_fp)
    return thumbnail

def resize_image(thumbnail):
    thumb_fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
    new_name = f'{os.path.splitext(os.path.basename(thumb_fp))[0]}.jpg'

    SIZE = (800, 800)
    LANCZOS = Image.LANCZOS
    
    with Image.open(thumb_fp) as img:
        img.convert('RGBA')

        img.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_name)
        img.save(thumb_io, 'jpeg', quality=85, optimize=True)

    os.remove(thumb_fp)
    return thumbnail
    