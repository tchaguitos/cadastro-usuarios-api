from rest_framework import viewsets, status
from rest_framework.response import Response

from locais.models import Cidade
from locais.serializers import CidadeSerializer


class CidadeViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Cidade.objects.select_related("estado", "estado__pais").all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CidadeSerializer(queryset, many=True)

        return Response(serializer.data)
