from django.contrib import admin

from locais.models import (
    Pais, Estado, Cidade
)

admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Cidade)

