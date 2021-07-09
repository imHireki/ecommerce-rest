from django.shortcuts import render
from rest_framework import viewsets
from .models import Produto, Variacao
from .serializers import ProdutoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all() 
    serializer_class = ProdutoSerializer 

    def destroy(self, request, pk, *args, **kwargs):
        # Getting the right object from queryset
        produto = self.get_queryset().filter(id=pk).first()
        # Destroying associated image when DELETE is called
        if produto.imagem:
            produto.imagem.delete(save=True)
        
        return super().destroy(request, *args, **kwargs)
