from django.contrib import admin
from .models import Produto, Variacao


class ProdutoAdmin(admin.ModelAdmin):
    pass

class VariacaoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
