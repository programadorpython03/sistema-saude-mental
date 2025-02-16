from django.db import models
from django.urls import reverse
# Create your models here.
class Pacientes(models.Model):
    
    queixas_choices = [
        ('TDHA', 'TDHA'),
        ('D', 'Depressao'),
        ('A', 'Ansiedade'),
        ('TAG', 'Transtorno de ansiedade generalizada'),
    ]

    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    pagamento_em_dia = models.BooleanField(default=True)
    queixa_principal = models.TextField(max_length=4, choices=queixas_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.nome

class Tarefas(models.Model):
    frequencia_choices = (
        ('D', 'Diário'),
        ('1S', '1 vez por semana'),
        ('2S', '2 vezes por semana'),
        ('3S', '3 vezes por semana'),
        ('N', 'Ao necessitar')
    )
    tarefa = models.CharField(max_length=255)
    instrucoes = models.TextField()
    frequencia = models.CharField(max_length=2, choices=frequencia_choices, default='D')

    def __str__(self):
        return self.tarefa

class Consultas(models.Model):
    humor = models.PositiveIntegerField()
    registro_geral = models.TextField()
    video = models.FileField(upload_to="video")
    tarefas = models.ManyToManyField(Tarefas)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.paciente.nome
    
    @property
    def link_publico(self):
        return f'http://localhost:8000/{reverse("consulta_publica", kwargs={"id": self.id})}'

class Visualizacoes(models.Model):
    consulta = models.ForeignKey(Consultas, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip} - {self.consulta}'
    
    @property
    def total_visualizacoes(self):
        return Visualizacoes.objects.filter(consulta=self).count()