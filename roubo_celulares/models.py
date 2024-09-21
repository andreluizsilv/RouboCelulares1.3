from django.db import models

class Bairro(models.Model):
    nome = models.CharField(max_length=255)  # Nome do bairro como um campo de texto
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.nome

class Roubo(models.Model):
    id_delegacia = models.IntegerField()
    data_ocorrencia_bo = models.DateField()
    hora_ocorrencia = models.TimeField(null=True, blank=True)
    descr_tipolocal = models.CharField(max_length=255)
    logradouro = models.CharField(max_length=255)
    numero_logradouro = models.CharField(max_length=255, default='Número padrão')

    # Campo bairro agora é uma ForeignKey para o modelo Bairro
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)  # Relaciona com o modelo Bairro

    cidade = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.logradouro}, {self.bairro.nome}'


class Feedback(models.Model):
    nome = models.CharField(max_length=100, default='Anonimo')
    email = models.EmailField(default='no-reply@example.com')
    experiencia = models.CharField(max_length=20, choices=[
        ('excelente', 'Excelente'),
        ('boa', 'Boa'),
        ('regular', 'Regular'),
        ('ruim', 'Ruim'),
    ])
    melhorias = models.CharField(
        max_length=20,
        choices=[
            ('nada', 'Nada'),
            ('pequenas', 'Pequenas mudanças'),
            ('moderadas', 'Mudanças moderadas'),
            ('grandes', 'Mudanças grandes'),
        ],
        default='nada'  # Definindo um valor padrão aqui
    )

    deixar_informacao = models.CharField(
        max_length=3,
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        default='nao'  # Definindo 'nao' como padrão
    )
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Nome: {self.nome} # Email:  {self.email} # Informação: {self.deixar_informacao}"

