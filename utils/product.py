"""
App product's useful functions
"""
from django.utils.text import slugify


def auto_slug(pk, name):
    """ Creates a slug concatenating `name` and `pk` / `id ` """
    dash_id = f'-{pk}'
    return slugify(name) + dash_id
