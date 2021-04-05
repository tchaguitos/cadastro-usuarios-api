from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from cadastro.models import Perfil

from cadastro.serializers import (
    CadastroSerializer, PerfilSerializer
)


class CadastroViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = CadastroSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "success": True,
                "message": "Perfil cadastrado com sucesso"
            }

            return Response(response, status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class PerfilViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            perfil = Perfil.objects.select_related("usuario", "municipio").get(
                usuario_id=request.user.id
            )

            perfil.get_nome()

            serializer = PerfilSerializer(perfil)

            return Response(serializer.data)

        except Exception as e:
            response = {
                "success": False,
                "message": str(e)
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
