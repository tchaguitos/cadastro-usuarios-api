from rest_framework import serializers
from locais.models import Cidade


class CidadeSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="get_nome_e_sigla")

    class Meta:
        model = Cidade
        fields = [
            "id", "nome"
        ]