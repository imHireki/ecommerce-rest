"""
Creating database tables:

- Produto
- Variacao
"""
from django.db import models
from django.utils.text import slugify
from PIL import Image
from django.conf.global_settings import MEDIA_ROOT


class Produto(models.Model):
    """ Produto database table """
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='img_produto/%Y/%m/', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField()
    # When not populated, it's gonna be represented as None on Python
    preco_marketing_promocional = models.FloatField(blank=True, null=True)
    tipo = models.CharField(
        default='S',
        max_length=1,
        choices=(
            ('S', 'Símples'),
            ('V', 'Variável'),
        ),
    )

    def __str__(self):
        """ Setting produto objects name in admin area """
        return self.nome

    @staticmethod
    def resize_save_image(img, new_width=int):
        """ Resize and save sent images """
        img_fp = img.path
        img_pil = Image.open(img_fp)
        (original_width, original_height) = img_pil.size
        
        # Just resize if original width > new_width 
        if not original_width > new_width:
            return
        
        # Figuring out new height
        new_height = round((new_width * original_height) / original_width)

        # Resizing with new values and a resample
        resized = img_pil.resize((new_width, new_height), Image.LANCZOS)
        resized.save(img_fp)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
            self.save()

        super().save(*args, **kwargs)

        if self.imagem: # Resizing image
            new_width = 800
            self.resize_save_image(self.imagem, new_width)


class Variacao(models.Model):
    """ Variacao database table """
    # Many (Variação) To One (Produto)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, blank=True, null=True)
    preco = models.FloatField()
    # When not populated, it's gonna be represented as None on Python
    preco_promocional = models.FloatField(blank=True, null=True)
    estoque = models.PositiveIntegerField(default=1)
    
    # Setting and fixing admin area's names
    def __str__(self):
        """ Setting and fixing produto objects name in admin area """
        return self.nome or self.produto.nome

    class Meta:
        """ Adjusting table names in admin area"""
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
