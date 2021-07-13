from rest_framework import serializers
from .models import Produto, Variacao


class ProdutoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'