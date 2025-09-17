from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from .models import Character, Planet

# простая главная
def index(request):
    characters = Character.objects.all()[:3]  # Получаем последних 3 персонажа
    planets = Planet.objects.all()[:3]  # Получаем последние 3 планеты
    data = {
        'title': 'Главная страница - Энциклопедия Star Wars',
        'characters': characters,
        'planets': planets,
    }
    return render(request, 'encyclopedia/index.html', context=data)

def characters(request):
    characters = Character.objects.all()  # Получаем всех персонажей
    data = {
        'title': 'Персонажи Star Wars',
        'characters': characters,
    }
    return render(request, 'encyclopedia/characters.html', context=data)

def planets(request):
    planets = Planet.objects.all()  # Получаем все планеты
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
        characters = Character.objects.filter(affiliation__icontains='Джедай')
    elif cat_id == 2:  # Ситхи
        characters = Character.objects.filter(affiliation__icontains='Ситхи')
    elif cat_id == 3:  # Повстанцы
        characters = Character.objects.filter(affiliation__icontains='Повстанцы')
    elif cat_id == 4:  # Империя
        characters = Character.objects.filter(affiliation__icontains='Империя')
    elif cat_id == 5:  # Сенаторы
        characters = Character.objects.filter(affiliation__icontains='Сенатор')
    elif cat_id == 6:  # Пилоты
        characters = Character.objects.filter(affiliation__icontains='Пилоты')
    else:
        characters = Character.objects.all()[:5]  
    
    context = {
        'title': f'{category_name} - Энциклопедия Star Wars',
        'category_name': category_name,
        'category_id': cat_id,
        'characters': characters
    }
    
    return render(request, 'encyclopedia/category.html', context)