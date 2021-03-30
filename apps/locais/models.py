from django.db import models

class Pais(models.Model):
    nome = models.CharField("nome", max_length=80)

    class Meta:
        verbose_name = "país"
        verbose_name_plural = "países"
        db_table = "pais"

    def __str__(self):
        return self.nome

class Estado(models.Model):
    pais = models.ForeignKey(
        Pais,
        verbose_name="país",
        on_delete=models.CASCADE,
    )

    nome = models.CharField("nome", max_length=80)
    sigla = models.CharField("sigla", max_length=2)

    def get_sigla(self):
        return self.sigla

    class Meta:
        verbose_name = "estado"
        verbose_name_plural = "estados"
        db_table = "estado"

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    estado = models.ForeignKey(
        Estado, 
        verbose_name="estado", 
        on_delete=models.CASCADE
    )

    nome = models.CharField("nome", max_length=80)

    def get_nome_e_sigla(self):
        return f"{ self.nome }/{ self.estado.get_sigla() }"

    class Meta:
        verbose_name = "cidade"
        verbose_name_plural = "cidades"
        db_table = "cidade"

    def __str__(self):
        return self.nome
