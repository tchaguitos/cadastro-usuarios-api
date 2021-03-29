from django.test import TestCase

from locais.models import (
    Pais, Estado, Cidade
)


class PaisTestCase(TestCase):

    def setUp(self):
        Pais.objects.create(
            nome="Brasil"
        )

    def test_instance(self):
        pais = Pais.objects.get(
            id=1
        )

        self.assertEqual(
            pais.__str__(),
            "Brasil"
        )

class EstadoTestCase(TestCase):

    def setUp(self):
        pais = Pais.objects.create(
            nome="Brasil"
        )
        
        Estado.objects.create(
            pais=pais,
            nome="Minas Gerais",
            sigla="MG"
        )

    def test_instance(self):
        estado = Estado.objects.get(
            id=1
        )

        self.assertEqual(
            estado.__str__(),
            "Minas Gerais"
        )

    def test_get_sigla(self):
        estado = Estado.objects.get(
            id=1
        )

        self.assertEqual(
            estado.get_sigla(),
            "MG"
        )

class CidadeTestCase(TestCase):

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

    def test_instance(self):
        cidade = Cidade.objects.get(
            id=1
        )

        self.assertEqual(
            cidade.__str__(),
            "Três Corações"
        )

    def test_get_nome_e_sigla(self):
        cidade = Cidade.objects.get(
            id=1
        )

        self.assertEqual(
            cidade.get_nome_e_sigla(),
            "Três Corações/MG"
        )
