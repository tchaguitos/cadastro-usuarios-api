from django.test import TestCase

from locais.models import (
    Pais, Estado, Cidade
)

from cadastro.models import Usuario, Perfil


class UsuarioTestCase(TestCase):

    def setUp(self):
        Usuario.objects.create_user(
            email="test@test.com",
            password="Test!@34",
            cpf="66444998050",
            pis="31756489822"
        )

    def test_instance(self):
        usuario = Usuario.objects.get(
            cpf="66444998050"
        )

        self.assertEqual(usuario.is_active, True)
        self.assertEqual(usuario.is_staff, False)
        self.assertEqual(usuario.is_superuser, False)

        self.assertEqual(
            usuario.__str__(),
            "test@test.com"
        )

        self.assertEqual(
            usuario.check_password("Test!@34"),
            True
        )

    def test_get_email(self):
        usuario = Usuario.objects.get(
            cpf="66444998050"
        )

        self.assertEqual(usuario.get_email(), "test@test.com")

    def test_get_cpf(self):
        usuario = Usuario.objects.get(
            cpf="66444998050"
        )

        self.assertEqual(usuario.get_cpf(), "66444998050")

    def test_get_pis(self):
        usuario = Usuario.objects.get(
            cpf="66444998050"
        )

        self.assertEqual(usuario.get_pis(), "31756489822")

class PerfilTestCase(TestCase):

    def setUp(self):
        pais = Pais.objects.create(
            nome="Brasil"
        )
        
        estado = Estado.objects.create(
            pais=pais,
            nome="Minas Gerais",
            sigla="MG"
        )

        cidade = Cidade.objects.create(
            estado=estado,
            nome="Três Corações",
        )

        usuario = Usuario.objects.create_user(
            email="test@test.com",
            password="Test!@34",
            cpf="66444998050",
            pis="31756489822"
        )

        Perfil.objects.create(
            usuario=usuario,
            nome_completo="Thiago Rodrigues Brasil",
            logradouro="Avenida Afonso Pena",
            numero=3693,
            complemento="Apartamento 385",
            cep="37410220",
            municipio=cidade
        )

    def test_instance(self):
        perfil = Perfil.objects.get(
            usuario__cpf="66444998050"
        )

        self.assertEqual(
            perfil.__str__(),
            "Thiago Rodrigues Brasil"
        )

    def test_get_email(self):
        perfil = Perfil.objects.get(
            usuario__cpf="66444998050"
        )

        self.assertEqual(
            perfil.get_email(),
            "test@test.com"
        )
