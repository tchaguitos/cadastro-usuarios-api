from django.db import IntegrityError, transaction

from rest_framework import serializers

from cadastro.models import Usuario, Perfil

from locais.serializers import CidadeSerializer

class PerfilSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="get_email")
    cpf = serializers.CharField(source="get_cpf")
    pis = serializers.CharField(source="get_pis")

    municipio = CidadeSerializer(source="get_municipio", many=False)

    nome = serializers.CharField(source="get_nome")


    class Meta:
        model = Perfil
        fields = [
            "email", "nome", "cpf", "pis", "token",
            "nome_completo", "logradouro", "numero",
            "complemento", "cep", "municipio"
        ]

class CadastroSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        error_messages = {
            "required": "Você deve fornecer um e-mail para se cadastrar",
        },
        required=True
    )

    cpf = serializers.CharField(
        error_messages={
            "required": "Você deve definir um CPF para se cadastrar"
        },
        required=True
    )

    pis = serializers.CharField(
        error_messages={
            "required": "Você deve definir um PIS para se cadastrar"
        },
        required=True
    )

    password = serializers.CharField(
        error_messages={
            "required": "Você deve definir uma senha para se cadastrar"
        },
        required=True
    )

    password2 = serializers.CharField(
        error_messages={
            "required": "Você deve definir uma senha para se cadastrar"
        },
        required=True
    )

    def validate_email(self, email):

        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este e-mail já está em uso")

        return email

    def validate_cpf(self, cpf):

        if Usuario.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError("Por favor, forneça outro CPF para continuar")

        return cpf

    def validate_pis(self, pis):

        if Usuario.objects.filter(pis=pis).exists():
            raise serializers.ValidationError("Por favor, forneça outro número de PIS para continuar")

        return pis

    def validate(self, data):

        password = data.get("password")
        password2 = data.get("password2")

        if password != password2:
            raise serializers.ValidationError({
                "password": "As senhas não conferem",
                "password2": "As senhas não conferem"
            })

        return data

    def save(self):

        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=self.validated_data["email"],
                    cpf=self.validated_data["cpf"],
                    pis=self.validated_data["pis"],
                    password=self.validated_data["password2"],
                )

                perfil = Perfil.objects.create(
                    usuario=usuario,
                    nome_completo=self.validated_data["nome_completo"],
                    logradouro=self.validated_data["logradouro"],
                    numero=self.validated_data["numero"],
                    complemento=self.validated_data["complemento"],
                    cep=self.validated_data["cep"],
                    municipio=self.validated_data["municipio"]
                )

                usuario.save()
                perfil.save()

        except IntegrityError:
            raise serializers.ValidationError("Ocorreu um erro. Por favor, tente novamente mais tarde")

        return perfil

    class Meta:
        model = Perfil
        fields = [
            "email", "cpf", "pis",
            "password", "password2",
            "nome_completo", "logradouro",
            "numero", "complemento", "cep",
            "municipio"
        ]
