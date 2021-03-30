from django.contrib import admin

from cadastro.models import (
    Usuario, Perfil
)

admin.site.register(Usuario)
admin.site.register(Perfil)
