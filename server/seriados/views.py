from re import template

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ReviewEpisodiosForm, RevisoresForm, SerieForm, TemporadaForm
from .models import (Blog, Categoria, Episodio, ReviewEpisodio, Revisor, Serie,
                     Temporada)


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

@login_required
@permission_required('seriados.view_episodio', raise_exception=True)
def episodios_details(resquest, pk):
    _object = get_object_or_404(Episodio, pk=pk)
    context = {
        'title': "Episódios",
        'data': prepare_data_detail(_object, ['titulo', 'data']),   
    }
    return render(resquest, 'details.html', context)
  
@login_required
@permission_required('seriados.view_episodio', raise_exception=True)
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

class EpisodioCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required='seriados.add_episodio'
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada','data','titulo']
    
class EpisodiosUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_episodio','seriados.change_episodio')
    template_name = 'form_generic.html'
    model = Episodio
    fields = ['temporada','data','titulo'] 
       
class EpisodiosDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required='seriados.delete_episodio'
    template_name = 'episodios_cohfirm_delete.html'
    model = Episodio
    
    def get_success_url(self):
        return reverse('seriados:episodios_list')


class EpisodiosBuscaLisView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required='seriados.view_episodio'
    template_name = 'episodios_busca_list.html'
    model = Episodio
    
    def get_queryset(self):
        search = self.request.GET.get('search', "")
        q = Q(titulo__contains=search) | Q(temporada__serie__nome__contains=search)
        for term in search.split():
            q = q | Q(titulo__contains=term)
            q = q | Q(temporada__serie__nome__contains=term)
            try:
                i_term = int(term)
            except ValueError:
                pass
            else:
                q = q | Q(temporada__numero=i_term)
        qs = super().get_queryset().filter(q)
        return qs

@login_required
@permission_required('seriados.view_revisor', raise_exception=True)
def revisores_details(resquest, pk):
    _object = get_object_or_404(Revisor, pk=pk)
    context = {
        'title': "Revisores",
        'data': prepare_data_detail(_object, ['user', 'reviews_episodios']),
    }
    return render(resquest, 'details.html', context)
  
@login_required
@permission_required('seriados.view_revisor', raise_exception=True)
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

class RevisoresCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'seriados.add_revisor'
    template_name = 'form_generic.html'
    form_class = RevisoresForm
    
class RevisoresUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_revisor','seriados.change_revisores')
    template_name = 'form_generic.html'
    model = Revisor
    fields = ['user','reviews_episodios']
    
class RevisoresDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required='seriados.delete_revisor'
    template_name = 'revisores_cohfirm_delete.html'
    model = Revisor
    
    def get_success_url(self):
        return reverse('seriados:revisores_list')

@login_required
@permission_required('seriados.view_reviewepisodio', raise_exception=True)
def review_episodios_details(resquest, pk):
    _object = get_object_or_404(ReviewEpisodio, pk=pk)
    context = {
        'title': "Review Episodios",
        'data': prepare_data_detail(_object, ['episodio', 'revisor','nota']),
    }
    return render(resquest, 'details.html', context)
  
@login_required
@permission_required('seriados.view_reviewepisodio', raise_exception=True)
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

    

class ReviewEpisodiosCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required='seriados.add_reviewepisodio'
    template_name = 'form_generic.html'
    form_class = ReviewEpisodiosForm
    
class ReviewEpisodiosUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_reviewepisodio','seriados.change_reviewepisodio')
    template_name = 'form_generic.html'
    model = ReviewEpisodio
    fields = ['episodio','revisor','nota']
    
class ReviewEpisodiosDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required='seriados.delete_reviewepisodio'
    template_name = 'revisores_episodios_cohfirm_delete.html'
    model = ReviewEpisodio
    
    def get_success_url(self):
        return reverse('seriados:review_episodios_list')

@login_required
@permission_required('seriados.view_episodio', raise_exception=True)
def episodio_nota_list(request, nota):
    objects = Episodio.objects.filter(reviewepisodio__nota=nota)
    context = {'objects': objects, 'nota':nota,}
    return render(request, 'episodio_nota_list.html', context)

class Contact(TemplateView):
    template_name= 'contact.html'

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})

class TemporadaListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required='seriados.view_temporada'
    template_name = 'temporada_list.html'
    model = Temporada
    
    def get_queryset(self):
        search = self.request.GET.get('search', "")
        q = Q(serie__nome__contains=search)
        for term in search.split():
            q = q | Q(serie__nome__contains=term)
            try:
                i_term = int(term)
            except ValueError:
                pass
            else:
                q = q | Q(numero=i_term)
        qs = super().get_queryset().filter(q)
        return qs
    
     
    
class TemporadaDetails(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    permission_required = 'seriados.view_temporada'
    template_name = 'temporada_details.html'
    model = Temporada
    
class TemporadaCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = 'seriados.add_temporada'
    template_name = 'form_generic.html'
    form_class = TemporadaForm
    
class TemporadaUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_temporada','seriados.change_temporada')
    template_name = 'form_generic.html'
    model = Temporada
    fields = ['serie','numero']
    
class TemporadaDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required='seriados.delete_temporada'
    template_name = 'temporada_cohfirm_delete.html'
    model = Temporada
    
    def get_success_url(self):
        return reverse('seriados:temporada_list')
    
class SerieListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = 'seriados.view_serie'
    template_name = 'series_list.html'
    model = Serie
    
    def get_queryset(self):
        search = self.request.GET.get('search', "")
        q = Q(nome__contains=search)
        for term in search.split():
            q = q | Q(nome__contains=term)
            try:
                i_term = int(term)
            except ValueError:
                pass
            else:
                q = q | Q(nome=i_term)
        qs = super().get_queryset().filter(q)
        return qs
        
class SerieDetailsView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    permission_required = 'seriados.view_serie'
    template_name = 'series_details.html'
    model = Serie
    
@login_required
@permission_required('seriados.add_serie', raise_exception=True)
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

class SeriesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('seriados.view_serie','seriados.change_serie')
    template_name = 'form_generic.html'
    model = Serie
    fields = ['nome']
    
class SeriesDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    permission_required = 'seriados.delete_serie'
    template_name = 'series_cohfirm_delete.html'
    model = Serie
    
    def get_success_url(self):
        return reverse('seriados:series_list')



def blog_list(request):
    categorias = Categoria.objects.all()
    posts = Blog.objects.all()[:5]
    context = {'categorias': categorias, 'posts':posts, 'detail_url_post': 'seriados:blog_post', 'detail_url_categorias': 'seriados:blog_categorias'}
    return render(request, 'blog.html', context)

def post_details(request, pk):
    _object = get_object_or_404(Blog, pk=pk)
    context = {
        'title': "Posts",
        'data': prepare_data_detail(_object, ['titulo', 'corpo','categoria']),
    }
    return render(request, 'post_details.html', context)




def categorias_details(request, pk):
    _object = get_object_or_404(Categoria, pk=pk)
    context = {
        'title': "Categorias",
        'data': prepare_data_detail(_object, ['titulo', 'url']),
        'posts': Blog.objects.filter(categoria=_object)[:5],
        'detail_url_post': 'seriados:blog_post'
    }
    return render(request, 'categorias_details.html', context)
