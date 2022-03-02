from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Serie(models.Model):
    nome = models.CharField(max_length=70, verbose_name="Nome")
    
    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"
      
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("seriados:series_details", kwargs={"pk": self.pk})
    
class Temporada(models.Model):
    numero = models.IntegerField(verbose_name="Número")
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE,verbose_name="Série")
    
    class Meta:
        verbose_name = "Temporada"
        verbose_name_plural = "Temporadas"
    
    def  __str__(self):
        return '%s %s' % (self.serie, self.numero)    

    
    def get_absolute_url(self):
        return reverse("seriados:temporadas_details", kwargs={"pk": self.pk})
    
class Episodio(models.Model):
    data = models.DateField(verbose_name="Data")
    titulo = models.CharField(max_length=200, verbose_name="Título")
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Episódio"
        verbose_name_plural = "Episódios"
    
    def __str__(self):
        return '%s %s %s' % (self.titulo, self.data,self.temporada)    
    
    def get_absolute_url(self):
        return reverse("seriados:episodios_details", kwargs={"pk": self.pk})
    
    
class Revisor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Revisores")
    reviews_episodios = models.ManyToManyField(Episodio,through='ReviewEpisodio')
    
    class Meta:
        verbose_name = "Revisor"
        verbose_name_plural = "Revisores"
    
    def __str__(self):
        return '%s %s' % (self.user, self.reviews_episodios)
    
    def get_absolute_url(self):
        return reverse("seriados:revisores_details", kwargs={"pk": self.pk})
    
class ReviewEpisodio(models.Model):
    NOTA_A = 'A'
    NOTA_B = 'B'
    NOTA_C = 'C'
    NOTAS_CHOICES = [
        (NOTA_A, _("Excelente")),
        (NOTA_B, _("Bom")),
        (NOTA_C, _("Ruim")),
    ]
    episodio = models.ForeignKey(Episodio, on_delete=models.CASCADE,verbose_name="Episódio")
    revisor = models.ForeignKey(Revisor,on_delete=models.CASCADE, verbose_name="Revisor")
    nota = models.CharField(
        max_length=1,
        choices=NOTAS_CHOICES,
        default=NOTA_B,
        verbose_name="Nota"
    )
    
    
    class Meta:
        verbose_name = "Review Episódio"
        verbose_name_plural = "Reviews Episódios"
    
    def __str__(self):
        return f"{self.episodio.titulo}: {self.revisor.user} : {self.nota}"
    
    def get_absolute_url(self):
        return reverse("seriados:review_episodios_details", kwargs={"pk": self.pk})
    

class Blog(models.Model):
    titulo = models.CharField(max_length=100, unique=True, verbose_name="Titulo")
    url = models.CharField(max_length=100, unique=True,verbose_name="Url")
    corpo = models.TextField( verbose_name="Corpo")
    data = models.DateField(db_index=True, auto_now_add=True,verbose_name="Data")
    categoria = models.ForeignKey('seriados.Categoria',on_delete=models.CASCADE, verbose_name="Categoria")

    def __str__(self):
        return '%s' % self.titulo

    def get_absolute_url(self):
        return reverse("seriados:blog_post", kwargs={"pk": self.pk})


class Categoria(models.Model):
    titulo = models.CharField(max_length=100, db_index=True, verbose_name="Titulo")
    url = models.CharField(max_length=100, db_index=True, verbose_name="Url")

    def __str__(self):
        return '%s' % self.titulo

    def get_absolute_url(self):
        return reverse("seriados:blog_categoria", kwargs={"pk": self.pk})

