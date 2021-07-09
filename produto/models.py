"""
Creating database tables:

- Produto
- Variacao
"""
from django.db import models
from django.db.models.fields import SlugField
from django.utils.text import slugify
from PIL import Image
from django.conf.global_settings import MEDIA_ROOT


class Produto(models.Model):
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

    # Setting admin area name
    def __str__(self):
        return self.nome

    @staticmethod
    def resize_image(img, new_width=int):
        img_fp = img.path
        img_pil = Image.open(img_fp)
        (original_width, original_height) = img_pil.size
        
        # Just resize if width > 800
        if not original_width > new_width:
            return
        
        # Figuring out new height
        new_height = round((new_width * original_height) / original_width)

        # Resizing with new values and a resample
        resized = img_pil.resize((new_width, new_height), Image.LANCZOS)
        resized.save(img_fp)

    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
            
        if self.imagem:
            new_width = 800
            self.resize_image(self.imagem, new_width)

        # Making the slugfield into a proper slug with a pk
        if not self.slug:
            self.slug = slugify(f'{self.nome} + {str(self.id)}')
            self.save()

    
class Variacao(models.Model):
    # Many (Variação) To One (Produto)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, blank=True, null=True)
    preco = models.FloatField()
    # When not populated, it's gonna be represented as None on Python
    preco_promocional = models.FloatField(blank=True, null=True)
    estoque = models.PositiveIntegerField(default=1)
    
    # Setting and fixing admin area's names
    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
