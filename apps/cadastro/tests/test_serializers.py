from django.test import TestCase

from locais.models import (
    Pais, Estado, Cidade
)

from cadastro.models import Usuario, Perfil

from cadastro.serializers import (
    PerfilSerializer, CadastroSerializer
)


class PerfilSerializerTestCase(TestCase):

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
            cep="37410555",
            municipio=cidade
        )

    def test_serializer(self):

        perfil = Perfil.objects.get(
            usuario__cpf="66444998050"
        )

        expected = {
            "email": "test@test.com",
            "nome": "Thiago",
            "cpf": "664.449.980-50",
            "pis": "317.56489.82-2",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": 3693,
            "complemento": "Apartamento 385",
            "cep": "37410-555",
            "municipio": {
                "id": 1,
                "nome": "Três Corações/MG"
            }
        }

        serializer = PerfilSerializer(instance=perfil)

        self.assertEqual(serializer.data, expected)

class CadastroSerializerTestCase(TestCase):

    def setUp(self):
        pais = Pais.objects.create(
            nome="Brasil"
        )
        
        estado = Estado.objects.create(
            pais=pais,
            nome="Minas Gerais",
            sigla="MG"
        )

        Cidade.objects.create(
            estado=estado,
            nome="Três Corações",
        )

    def cadastro_usuario_teste(self):

        usuario = Usuario.objects.create_user(
            email="help@test.com",
            password="Test!@34",
            cpf="66444998050",
            pis="31756489822",
        )

        cidade = Cidade.objects.get(
            id=1
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

    def test_serializer_is_valid(self):
        data = {
            "email": "tchaguitos@gmail.com",
            "cpf": "66444998050",
            "pis": "31756489822",
            "password": "Test!@34",
            "password2": "Test!@34",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": "4021",
            "complemento": "Apartamento 405",
            "cep": "38410321",
            "municipio": "1"
        }

        serializer = CadastroSerializer(data=data)

        self.assertEqual(serializer.is_valid(), True)

    def test_serializer_email_existente(self):

        self.cadastro_usuario_teste()

        data = {
            "email": "help@test.com",
            "cpf": "66444998022",
            "pis": "31756489822",
            "password": "Test!@34",
            "password2": "Test!@34",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": "4021",
            "complemento": "Apartamento 405",
            "cep": "38410321",
            "municipio": "1"
        }

        serializer = CadastroSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertEqual(
            is_valid,
            False
        )

        self.assertEqual(
            serializer.errors["email"][0],
            "Este e-mail já está em uso"
        )

    def test_serializer_cpf_existente(self):

        self.cadastro_usuario_teste()

        data = {
            "email": "help2@test.com",
            "cpf": "66444998050",
            "pis": "31756289812",
            "password": "Test!@34",
            "password2": "Test!@34",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": "4021",
            "complemento": "Apartamento 405",
            "cep": "38410321",
            "municipio": "1"
        }

        serializer = CadastroSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertEqual(
            is_valid,
            False
        )

        self.assertEqual(
            serializer.errors["cpf"][0],
            "Por favor, forneça outro CPF para continuar"
        )

    def test_serializer_pis_existente(self):

        self.cadastro_usuario_teste()

        data = {
            "email": "help2@test.com",
            "cpf": "66444998022",
            "pis": "31756489822",
            "password": "Test!@34",
            "password2": "Test!@34",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": "4021",
            "complemento": "Apartamento 405",
            "cep": "38410321",
            "municipio": "1"
        }

        serializer = CadastroSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertEqual(
            is_valid,
            False
        )

        self.assertEqual(
            serializer.errors["pis"][0],
            "Por favor, forneça outro número de PIS para continuar"
        )

    def test_serializer_senhas_diferentes(self):
        data = {
            "email": "tchaguitos@gmail.com",
            "cpf": "66444998050",
            "pis": "31756489822",
            "password": "Test!@34",
            "password2": "Test!@3",
            "nome_completo": "Thiago Rodrigues Brasil",
            "logradouro": "Avenida Afonso Pena",
            "numero": "4021",
            "complemento": "Apartamento 405",
            "cep": "38410321",
            "municipio": "1"
        }

        serializer = CadastroSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertEqual(
            is_valid,
            False
        )

        self.assertEqual(
            serializer.errors["password"][0], "As senhas não conferem"
        )

        self.assertEqual(
            serializer.errors["password2"][0], "As senhas não conferem"
        )