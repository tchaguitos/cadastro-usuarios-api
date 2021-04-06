from django.test import TestCase

from locais.models import (
    Pais, Estado, Cidade
)

from locais.serializers import CidadeSerializer


class CidadeSerializerTestCase(TestCase):

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

    def test_serializer(self):

        cidade = Cidade.objects.get(
            id=1
        )

        expected = {
            "id": 1,
            "nome": "Três Corações/MG"
        }

        serializer = CidadeSerializer(instance=cidade)

        self.assertEqual(serializer.data, expected)
