from django.urls import include, path, re_path, register_converter
from django.views.generic import TemplateView

from . import views

app_name = 'seriados'

urlpatterns = [
    #path('series/',views.series_list, name='series_list'),
    #path('series/<int:pk>/', views.series_details, name='series_details'),

    
    path('episodios/',views.episodios_list,name='episodios_list'),
    path('episodios/<int:pk>/', views.episodios_details, name='episodios_details'),
    path('episodios/inserir/', views.EpisodioCreateView.as_view(),name='episodios_insert'),
    path('episodios/<int:pk>/editar', views.EpisodiosUpdateView.as_view(),name='episodios_update'),
    path('episodios/<int:pk>/excluir/', views.EpisodiosDeleteView.as_view(),name='episodios_excluir'),
    
    path('episodios/nota/<str:nota>/', views.episodio_nota_list,name='episodio_nota_list'),
    
    path('revisores/',views.revisores_list,name='revisores_list'),
    path('revisores/<int:pk>/', views.revisores_details, name='revisores_details'),
    path('revisores/inserir/', views.RevisoresCreateView.as_view(), name='revisores_insert'),
    path('revisores/<int:pk>/editar', views.RevisoresUpdateView.as_view(),name='revisores_update'),
    path('revisores/<int:pk>/excluir/', views.RevisoresDeleteView.as_view(),name='revisores_excluir'),
    
    path('review_episodios/',views.review_episodios_list,name='review_episodios_list'),
    path('review_episodios/<int:pk>/', views.review_episodios_details, name='review_episodios_details'),
    path('review_episodios/inserir/', views.ReviewEpisodiosCreateView.as_view(), name='review_episodios_insert'),
    path('review_episodios/<int:pk>/editar', views.ReviewEpisodiosUpdateView.as_view(),name='review_episodios_update'),
    path('review_episodios/<int:pk>/excluir/', views.ReviewEpisodiosDeleteView.as_view(),name='review_episodios_excluir'),
    
    path('sobre/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('contato/', views.Contact.as_view(), name='contact'),
   
    path('home', views.HomeView.as_view(), name='home'),
    
    path('temporadas/', views.TemporadaListView.as_view(), name='temporadas_list'),
    path('temporadas/<int:pk>/', views.TemporadaDetails.as_view(), name='temporadas_details'),
    path('temporadas/inserir/', views.TemporadaCreateView.as_view(), name='temporadas_insert'),
    path('temporadas/<int:pk>/editar', views.TemporadaUpdateView.as_view(),name='temporadas_update'),
    path('temporadas/<int:pk>/excluir/', views.TemporadaDeleteView.as_view(),name='temporadas_excluir'),
    
    path('series/', views.SerieListView.as_view(), name='series_list'),
    path('series/<int:pk>/', views.SerieDetailsView.as_view(), name='series_details'),
    path('series/inserir/',views.series_insert, name='series_insert'),
    path('series/<int:pk>/editar', views.SeriesUpdateView.as_view(),name='series_update'),
    path('series/<int:pk>/excluir/', views.SeriesDeleteView.as_view(),name='series_excluir'),
  
   ]   
