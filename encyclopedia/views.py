from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from .models import Character, Planet, Tag, Faction
from django.db.models import Q, F, Value, Count, Avg, Max, Min, CharField, BooleanField, IntegerField
from django.db.models.functions import Concat

# простая главная
def index(request):
    characters = Character.published.all()[:3]
    planets = Planet.published.all()[:3]
    data = {
        'title': 'Главная страница - Энциклопедия Star Wars',
        'characters': characters,
        'planets': planets,
    }
    return render(request, 'encyclopedia/index.html', context=data)

def characters(request):
    characters = Character.published.all()
    data = {
        'title': 'Персонажи Star Wars',
        'characters': characters,
    }
    return render(request, 'encyclopedia/characters.html', context=data)

def planets(request):
    planets = Planet.published.all()
    data = {
        'title': 'Планеты Star Wars',
        'planets': planets,
    }
    return render(request, 'encyclopedia/planets.html', context=data)

def search(request):
    query = request.GET.get('q', '').strip()
    characters = Character.objects.none()
    planets = Planet.objects.none()
    if query:
        characters = Character.objects.filter(name__icontains=query)
        planets = Planet.objects.filter(name__icontains=query)
    context = {
        'title': 'Поиск',
        'query': query,
        'characters': characters,
        'planets': planets,
    }
    return render(request, 'encyclopedia/search_results.html', context)

# динамический URL: по slug
def character_detail(request, character_slug):
    character = get_object_or_404(Character, slug=character_slug)
    data = {
        'title': character.name,
        'character': character,
    }
    return render(request, 'encyclopedia/character_detail.html', context=data)

# динамический URL: по slug
def planet_detail(request, planet_slug):
    planet = get_object_or_404(Planet, slug=planet_slug)
    data = {
        'title': planet.name,
        'planet': planet,
    }
    return render(request, 'encyclopedia/planet_detail.html', context=data)
    
def code_view(request, swcode):
    return HttpResponse(f"Вы обратились к объекту с кодом {swcode}")

def start(request):
    return redirect('home')

def error_404(request, exception):
    return HttpResponse("<h1>Ошибка 404 — Страница не найдена</h1>", status=404)

def error_500(request):
    return HttpResponse("<h1>Ошибка 500 — Внутренняя ошибка сервера</h1>", status=500)

def get_character(request):
    # Проверяем, что метод GET
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    # Получаем имя персонажа из query-параметра
    name = request.GET.get("name", "").strip()
    if not name:
        return HttpResponse("<h1>Ошибка: укажите имя персонажа через ?name=Имя</h1>", status=400)

    # Пытаемся найти персонажа по имени (регистронезависимо)
    try:
        character = Character.objects.get(name__iexact=name)
        return HttpResponse(f"<h1>Персонаж: {character.name}</h1>")
    except Character.DoesNotExist:
        return HttpResponse("<h1>Ошибка 404 — Персонаж не найден</h1>", status=404)

def category(request, cat_id):
    """Страница категории персонажей"""
    categories = {
        1: 'Джедаи',
        2: 'Ситхи', 
        3: 'Повстанцы',
        4: 'Империя',
        5: 'Сенаторы',
        6: 'Пилоты'
    }
    
    category_name = categories.get(cat_id, 'Неизвестная категория')
    
    # Фильтруем персонажей по категории 
    if cat_id == 1:  # Джедаи
        characters = Character.published.filter(affiliation__icontains='Джедай')
    elif cat_id == 2:  # Ситхи
        characters = Character.published.filter(affiliation__icontains='Ситхи')
    elif cat_id == 3:  # Повстанцы
        characters = Character.published.filter(affiliation__icontains='Повстанцы')
    elif cat_id == 4:  # Империя
        characters = Character.published.filter(affiliation__icontains='Империя')
    elif cat_id == 5:  # Сенаторы
        characters = Character.published.filter(affiliation__icontains='Сенатор')
    elif cat_id == 6:  # Пилоты
        characters = Character.published.filter(affiliation__icontains='Пилоты')
    else:
        characters = Character.published.all()[:5]  
    
    context = {
        'title': f'{category_name} - Энциклопедия Star Wars',
        'category_name': category_name,
        'category_id': cat_id,
        'characters': characters
    }
    
    return render(request, 'encyclopedia/category.html', context)
def tags_list(request):
    tags = Tag.objects.all().annotate(
        total_characters=Count('characters'),
        total_planets=Count('planets')
    )
    data = {
        'title': 'Теги',
        'tags': tags,
    }
    return render(request, 'encyclopedia/tags_list.html', context=data)

def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    characters = Character.published.filter(tags=tag)
    planets = Planet.published.filter(tags=tag)
    data = {
        'title': f'Тег: {tag.name}',
        'tag': tag,
        'characters': characters,
        'planets': planets,
    }
    return render(request, 'encyclopedia/tag_detail.html', data)

def reports(request):
    jedi_or_rebels = Character.published.filter(
        Q(affiliation__icontains='Джедай') | Q(affiliation__icontains='Повстанцы')
    ).annotate(
        full_title=Concat(Value('Персонаж: '), F('name'))
    )

    residents_by_planet = Planet.published.annotate(
        residents_count=Count('residents')
    ).order_by('-residents_count')

    stats = Character.published.aggregate(
        total=Count('id'),
        max_midichlorians=Max('detail__midichlorians'),
        min_midichlorians=Min('detail__midichlorians'),
        avg_midichlorians=Avg('detail__midichlorians'),
    )

    # Примеры использования Value: константные поля и вычисления на стороне БД
    with_value = Character.published.annotate(
        kind=Value('character', output_field=CharField()),
        is_featured=Value(True, output_field=BooleanField()),
        score=(F('detail__midichlorians') + Value(1000, output_field=IntegerField()))
    ).values('name', 'kind', 'is_featured', 'score')[:10]

    data = {
        'title': 'Отчеты',
        'jedi_or_rebels': jedi_or_rebels,
        'residents_by_planet': residents_by_planet,
        'stats': stats,
        'with_value': with_value,
    }
    return render(request, 'encyclopedia/reports.html', data)
    
    context = {
        'title': f'{category_name} - Энциклопедия Star Wars',
        'category_name': category_name,
        'category_id': cat_id,
        'characters': characters
    }
    
    return render(request, 'encyclopedia/category.html', context)