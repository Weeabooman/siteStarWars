from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from .models import Character, Planet

# простая главная
def index(request):
    return render(request, 'encyclopedia/index.html')

def characters(request):
    qs = Character.objects.all()
    return render(request, 'encyclopedia/characters.html', {'characters': qs})

def planets(request):
    qs = Planet.objects.all()
    return render(request, 'encyclopedia/planets.html', {'planets': qs})

# динамический URL: по ID
def character_detail(request, char_id):
    # пока без БД, просто тестовый вывод
    return HttpResponse(f"<h3>Вы открыли персонажа с ID = {char_id}</h3>")

# динамический URL: по имени
def planet_detail(request, name):
    planets = ["Tatooine", "Alderaan", "Naboo"]
    if name in planets:
        return HttpResponse(f"<h3>Планета: {name}</h3>")
    else:
        # обработка ошибки
        raise Http404(f"Планета {name} не найдена")
    
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