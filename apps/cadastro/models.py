from uuid import uuid4

from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UsuarioManager(BaseUserManager):

    def create_user(self, email, cpf, pis, password=None):
        user = self.model(
            email=self.normalize_email(email),
            cpf=cpf,
            pis=pis
        )

        user.is_active = True
        user.is_staff = False
        user.is_superuser = False

        if password:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, cpf, pis, password):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            cpf=cpf,
            pis=pis
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)

        return user

class Usuario(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name="E-mail",
        max_length=184,
        unique=True
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
        unique=True,
    )

    pis = models.CharField(
        verbose_name="PIS",
        max_length=11,
        unique=True,
    )

    is_active = models.BooleanField(
        verbose_name="O usuário está ativo?",
        default=True
    )

    is_staff = models.BooleanField(
        verbose_name="O usuário é membro da equipe?",
        default=False
    )

    is_superuser = models.BooleanField(
        verbose_name="O usuário é um super usuário?",
        default=False
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["cpf", "pis"]

    def get_email(self):
        return self.email

    def get_cpf(self):
        return self.cpf

    def get_pis(self):
        return self.pis

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

class Perfil(models.Model):

    token = models.UUIDField(default=uuid4)

    usuario = models.OneToOneField(
        "cadastro.Usuario",
        verbose_name="Usuário vinculado ao perfil",
        on_delete=models.PROTECT
    )

    nome_completo = models.CharField(
        verbose_name="Nome completo",
        max_length=254
    )

    logradouro = models.CharField(
        verbose_name="Logradouro",
        max_length=84
    )

    numero = models.IntegerField(
        verbose_name="Número"
    )

    complemento = models.CharField(
        verbose_name="Complemento",
        max_length=94,
        blank=True
    )

    cep = models.CharField(
        verbose_name="CEP",
        max_length=9
    )

    municipio = models.ForeignKey(
        "locais.Cidade",
        verbose_name="Cidade",
        on_delete=models.PROTECT
    )

    def get_email(self):
        return self.usuario.email

    def get_nome(self):
        primeiro_nome = self.nome_completo.split(" ")[0]
        return primeiro_nome

    def get_cpf(self):
        cpf = self.usuario.cpf
        cpf_mascarado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

        return cpf_mascarado

    def get_pis(self):
        pis = self.usuario.pis
        pis_mascarado = f"{pis[:3]}.{pis[3:8]}.{pis[8:10]}-{pis[10:]}"

        return pis_mascarado

    def get_municipio(self):
        return self.municipio

    class Meta:
        db_table = "perfil"
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return self.nome_completo
