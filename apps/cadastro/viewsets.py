from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from cadastro.models import Perfil

from cadastro.serializers import (
    CadastroSerializer, PerfilSerializer, AtualizaPerfilSerializer
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

    def get_queryset(self):
        return Perfil.objects.select_related("usuario", "municipio").all()

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

    def update(self, request, pk=None):

        id_usuario = request.user.perfil.id

        perfil = get_object_or_404(
            self.get_queryset(),
            pk=id_usuario
        )

        serializer = AtualizaPerfilSerializer(perfil, data=request.data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "success": True,
                "message": "Perfil atualizado com sucesso"
            }

            return Response(response, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
