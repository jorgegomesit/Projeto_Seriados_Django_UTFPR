from django import forms

from .models import Episodio, ReviewEpisodio, Revisor, Serie, Temporada


class SerieForm(forms.Form):
    nome = forms.CharField(label="Nome da Série", max_length=70)

class TemporadaForm(forms.ModelForm):
    
    class Meta:
        model = Temporada
        fields = ['numero','serie']

class RevisoresForm(forms.ModelForm):
    
    class Meta:
        model = Revisor
        fields = ['user','reviews_episodios']

class ReviewEpisodiosForm(forms.ModelForm):
    
    class Meta:
        model = ReviewEpisodio
        fields = ['episodio','revisor','nota']
