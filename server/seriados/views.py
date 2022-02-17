from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ReviewEpisodiosForm, RevisoresForm, SerieForm, TemporadaForm
from .models import Episodio, ReviewEpisodio, Revisor, Serie, Temporada


def prepare_data_list(objects, fields_name):
    labels = list()
    for field_name in fields_name:
        field = objects.model._meta.get_field(field_name)
        labels.append(field.verbose_name)
    
    rows = list()
    for _object in objects:
        row = dict()
        rows.append(row)
        row['pk'] = _object.pk
        row['data'] = list()
        for field_name in fields_name:
            row['data'].append(getattr(_object, field_name))
    
    return labels, rows


def prepare_data_detail(_object, fields_name):
    data = model_to_dict(_object)
    rows = list()
    for field_name in fields_name:
        field = _object._meta.get_field(field_name)
        rows.append({'label': field.verbose_name, 'value': data[field_name]})
    return rows

def episodios_details(resquest, pk):
    _object = get_object_or_404(Episodio, pk=pk)
    context = {
        'title': "Episódios",
        'data': prepare_data_detail(_object, ['titulo', 'data']),   
    }
    return render(resquest, 'details.html', context)
  

def episodios_list(request):
    search = request.GET.get('search',"")
    objects = Episodio.objects.filter(titulo__contains=search)
    labels, rows = prepare_data_list(objects,['titulo','data'] )
    context = {
        'title': "Episódios",
        'labels': labels,
        'rows': rows,
        'detail_url': 'seriados:episodios_details',
        'list_url': 'seriados:episodios_list',
    }
    return render(request, 'list.html', context)

class EpisodioCreateView(CreateView):
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada','data','titulo']
    
class EpisodiosUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada','data','titulo'] 
       
class EpisodiosDeleteView(DeleteView):
    template_name = 'episodios_cohfirm_delete.html'
    model = Episodio
    
    def get_success_url(self):
        return reverse('seriados:episodios_list')

def revisores_details(resquest, pk):
    _object = get_object_or_404(Revisor, pk=pk)
    context = {
        'title': "Revisores",
        'data': prepare_data_detail(_object, ['user', 'reviews_episodios']),
    }
    return render(resquest, 'details.html', context)
  

def revisores_list(request):
    search = request.GET.get('search',"")
    if search == "" :
        objects = Revisor.objects.all()
    else:
        objects = Revisor.objects.filter(user_id=search)
    
    labels, rows = prepare_data_list(objects,['user'] )
    context = {
            'title': "Revisores",
            'labels': labels,
            'rows': rows,
            'detail_url': 'seriados:revisores_details',
            'list_url': 'seriados:revisores_list',

    }
    return render(request, 'list.html', context)

class RevisoresCreateView(CreateView):
    template_name = 'form_generic.html'
    form_class = RevisoresForm
    
class RevisoresUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Revisor
    fields = ['user','reviews_episodios']
    
class RevisoresDeleteView(DeleteView):
    template_name = 'revisores_cohfirm_delete.html'
    model = Revisor
    
    def get_success_url(self):
        return reverse('seriados:revisores_list')

def review_episodios_details(resquest, pk):
    _object = get_object_or_404(ReviewEpisodio, pk=pk)
    context = {
        'title': "Review Episodios",
        'data': prepare_data_detail(_object, ['episodio', 'revisor','nota']),
    }
    return render(resquest, 'details.html', context)
  

def review_episodios_list(request):
    search = request.GET.get('search',"")
    if search == "" :
        objects = ReviewEpisodio.objects.all()
    else:
        objects = ReviewEpisodio.objects.filter(episodio_id=search)
        
    labels, rows = prepare_data_list(objects,['episodio','revisor','nota'] )
    context = {
        'title': "Review Episodios",
        'labels': labels,
        'rows': rows,
        'detail_url': 'seriados:review_episodios_details',
        'list_url': 'seriados:review_episodios_list',

    }
    return render(request, 'list.html', context)

class ReviewEpisodiosCreateView(CreateView):
    template_name = 'form_generic.html'
    form_class = ReviewEpisodiosForm
    
class ReviewEpisodiosUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = ReviewEpisodio
    fields = ['episodio','revisor','nota']
    
class ReviewEpisodiosDeleteView(DeleteView):
    template_name = 'revisores_episodios_cohfirm_delete.html'
    model = ReviewEpisodio
    
    def get_success_url(self):
        return reverse('seriados:revisores_list')

def episodio_nota_list(request, nota):
    objects = Episodio.objects.filter(reviewepisodio__nota=nota)
    context = {'objects': objects, 'nota':nota,}
    return render(request, 'episodio_nota_list.html', context)

class Contact(TemplateView):
    template_name= 'contact.html'

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})

class TemporadaListView(ListView):
    template_name = 'temporada_list.html'
    model = Temporada
    
    
class TemporadaDetails(DetailView):
    template_name = 'temporada_details.html'
    model = Temporada
    
class TemporadaCreateView(CreateView):
    template_name = 'form_generic.html'
    form_class = TemporadaForm
    
class TemporadaUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Temporada
    fields = ['serie','numero']
    
class TemporadaDeleteView(DeleteView):
    template_name = 'temporada_cohfirm_delete.html'
    model = Temporada
    
    def get_success_url(self):
        return reverse('seriados:temporada_list')
    
class SerieListView(ListView):
    template_name = 'series_list.html'
    model = Serie
        
class SerieDetailsView(DetailView):
    template_name = 'series_details.html'
    model = Serie

def series_insert(request):
    if  request.method == 'GET':
        form = SerieForm()
    elif request.method == 'POST':
        form = SerieForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            obj = Serie(nome = nome)
            obj.save()
            return HttpResponseRedirect(reverse(
                'seriados:series_details',
                kwargs= {'pk': obj.pk}
            ))
    return render(request,'form_base.html', {
        'form': form,
        'target_url': 'seriados:series_insert',
    })

class SeriesUpdateView(UpdateView):
    template_name = 'form_generic.html'
    model = Serie
    fields = ['nome']
    
class SeriesDeleteView(DeleteView):
    template_name = 'series_cohfirm_delete.html'
    model = Serie
    
    def get_success_url(self):
        return reverse('seriados:series_list')
