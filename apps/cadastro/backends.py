from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from django.db.models import Q

from cadastro.models import Usuario


class CustomBackend(BaseBackend):

    def get_user(self, user_id):

        try:
            return Usuario.objects.get(pk=user_id)

        except Usuario.DoesNotExist:
            return None

    def authenticate(self, request, email=None, password=None):

        try:
            usuario = Usuario.objects.get(
                Q(email=email) | Q(cpf=email) | Q(pis=email)
            )

        except Usuario.DoesNotExist:
            return None

        password_valid = usuario.check_password(password)

        if password_valid:
            return usuario

        return None
