from django.urls import path, register_converter
from . import views
from .converters import SWCodeConverter

# регистрируем конвертер
register_converter(SWCodeConverter, 'sw')

urlpatterns = [
    path('', views.index, name='home'),
    path('characters/', views.characters, name='characters'),
    path('planets/', views.planets, name='planets'),
    path('search/', views.search, name='search'),
    path('tags/', views.tags_list, name='tags_list'),
    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),
    path('reports/', views.reports, name='reports'),
    path('character/<slug:character_slug>/', views.character_detail, name='character_detail'),
    path('planet/<slug:planet_slug>/', views.planet_detail, name='planet_detail'),
    # собственный конвертер
    path('code/<sw:swcode>/', views.code_view, name='code_view'),
    path('start/', views.start, name='start'),
    path('get-character/', views.get_character, name='get_character'),
    # категории персонажей
    path('category/<int:cat_id>/', views.category, name='category'),
]