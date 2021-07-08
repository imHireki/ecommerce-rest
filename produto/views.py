from django.shortcuts import render
from rest_framework import viewsets
from .models import Produto, Variacao
from .serializers import ProdutoSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all() 
    serializer_class = ProdutoSerializer 
