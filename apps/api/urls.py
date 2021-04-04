from django.urls import path, include
from rest_framework import routers

from locais.viewsets import CidadeViewSet

from cadastro.viewsets import (
    CadastroViewSet, PerfilViewSet
)

router = routers.DefaultRouter()

router.register(
    "cidades",
    CidadeViewSet,
    basename="cidade"
)

router.register(
    "cadastro",
    CadastroViewSet,
    basename="cadastro"
)

urlpatterns = [
    path("", include(router.urls)),
    path("perfil/", PerfilViewSet.as_view({'get': 'get'}), name="perfil")
]
