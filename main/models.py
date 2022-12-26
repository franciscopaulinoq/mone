from django.db import models

# Create your models here.

LISTA_TIPO = [
    ('Receita', 'Receita'),
    ('Gasto', 'Gasto'),
]

class Categoria(models.Model):
    nome = models.CharField(max_length = 50)
    tipo = models.CharField(max_length = 50, choices = LISTA_TIPO, default = 'Receita')
    cor = models.CharField(max_length = 7)

    def __str__(self):
        return self.nome

class Receita(models.Model):
    valor = models.DecimalField('Valor', max_digits = 8, decimal_places = 2)
    data = models.DateField()
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.valor)

class Gasto(models.Model):
    valor = models.DecimalField('Valor', max_digits = 8, decimal_places = 2)
    data = models.DateField()
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.valor)