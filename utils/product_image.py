from django.core.files.images import File
from django.conf import settings

from io import BytesIO
from PIL import Image
import os

from apps.product import models


def resize_thumbnail(thumbnail):
    thumb_fp = os.path.join(
        settings.MEDIA_ROOT, thumbnail.name
    )
    thumb_name = os.path.basename(thumb_fp)
    thumb_basename = os.path.splitext(thumb_name)[0]
    new_basename = f'{thumb_basename}.png'

    SIZE = (228, 228)
    LANCZOS = Image.LANCZOS
    
    with Image.open(thumb_fp) as img:
        img.convert('RGBA')
        img.thumbnail(SIZE, LANCZOS)

        thumb_io = BytesIO()
        thumbnail = File(thumb_io, name=new_basename)
        img.save(thumb_io, 'PNG', quality=85, optimize=True)

    os.remove(thumb_fp)
    return thumbnail
