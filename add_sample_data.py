#!/usr/bin/env python
"""
Скрипт для добавления тестовых данных в базу данных Star Wars Encyclopedia
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteStarWars.settings')
django.setup()

from encyclopedia.models import Character, Planet

def add_planets():
    """Добавление планет в базу данных"""
    planets_data = [
        {
            'name': 'Татуин',
            'slug': 'tatooine',
            'system': 'Система Татуин',
            'description': 'Пустынная планета с двумя солнцами, родина Люка Скайуокера и Энакина Скайуокера.',
            'population': 200000,
            'climate': 'Пустынный',
            'is_published': Planet.Status.PUBLISHED
        },
        {
            'name': 'Алдераан',
            'slug': 'alderaan',
            'system': 'Система Алдераан',
            'description': 'Красивая планета, уничтоженная Звездой Смерти. Родина принцессы Леи.',
            'population': 2000000000,
            'climate': 'Умеренный',
            'is_published': Planet.Status.PUBLISHED
        },
        {
            'name': 'Корусант',
            'slug': 'coruscant',
            'system': 'Система Корусант',
            'description': 'Столица Галактической Республики и Империи. Планета-город.',
            'population': 1000000000000,
            'climate': 'Умеренный',
            'is_published': Planet.Status.PUBLISHED
        },
        {
            'name': 'Набу',
            'slug': 'naboo',
            'system': 'Система Набу',
            'description': 'Красивая планета с озерами и лугами. Родина Падме Амидалы.',
            'population': 4500000000,
            'climate': 'Умеренный',
            'is_published': Planet.Status.PUBLISHED
        },
        {
            'name': 'Кашиик',
            'slug': 'kashyyyk',
            'system': 'Система Кашиик',
            'description': 'Планета вуки с огромными деревьями. Родина Чубакки.',
            'population': 45000000,
            'climate': 'Тропический',
            'is_published': Planet.Status.PUBLISHED
        }
    ]
    
    for planet_data in planets_data:
        planet, created = Planet.objects.get_or_create(
            name=planet_data['name'],
            defaults=planet_data
        )
        if created:
            print(f"Создана планета: {planet.name}")
        else:
            print(f"Планета уже существует: {planet.name}")
    
    return Planet.objects.all()

def add_characters():
    """Добавление персонажей в базу данных"""
    characters_data = [
        {
            'name': 'Люк Скайуокер',
            'slug': 'luke-skywalker',
            'species': 'Человек',
            'affiliation': 'Джедай',
            'description': 'Сын Энакина Скайуокера и Падме Амидалы. Последний джедай, который восстановил Орден.',
            'is_published': Character.Status.PUBLISHED
        },
        {
            'name': 'Лея Органа',
            'slug': 'leia-organa',
            'species': 'Человек',
            'affiliation': 'Повстанцы',
            'description': 'Принцесса Алдераана, лидер Повстанческого Альянса. Сестра Люка Скайуокера.',
            'is_published': Character.Status.PUBLISHED
        },
        {
            'name': 'Дарт Вейдер',
            'slug': 'darth-vader',
            'species': 'Человек',
            'affiliation': 'Ситхи',
            'description': 'Темный лорд ситхов, бывший Энакин Скайуокер. Отец Люка и Леи.',
            'is_published': Character.Status.PUBLISHED
        },
        {
            'name': 'Оби-Ван Кеноби',
            'slug': 'obi-wan-kenobi',
            'species': 'Человек',
            'affiliation': 'Джедай',
            'description': 'Джедай-мастер, наставник Энакина Скайуокера. Один из величайших джедаев.',
            'is_published': Character.Status.PUBLISHED
        },
        {
            'name': 'Йода',
            'slug': 'yoda',
            'species': 'Неизвестно',
            'affiliation': 'Джедай',
            'description': 'Мудрый джедай-мастер, один из самых сильных в Силе. Наставник Люка Скайуокера.',
            'is_published': Character.Status.PUBLISHED
        }
    ]
    
    # Получаем планеты для связывания
    tatooine = Planet.objects.get(name='Татуин')
    alderaan = Planet.objects.get(name='Алдераан')
    coruscant = Planet.objects.get(name='Корусант')
    naboo = Planet.objects.get(name='Набу')
    
    # Добавляем связи с планетами
    characters_data[0]['homeworld'] = tatooine  # Люк Скайуокер
    characters_data[1]['homeworld'] = alderaan  # Лея Органа
    characters_data[3]['homeworld'] = tatooine  # Дарт Вейдер (Энакин)
    characters_data[4]['homeworld'] = coruscant  # Оби-Ван Кеноби
    # characters_data[6]['homeworld'] = naboo  # Император Палпатин (индекс не существует)
    for character_data in characters_data:
        character, created = Character.objects.get_or_create(
            name=character_data['name'],
            defaults=character_data
        )
        if created:
            print(f"Создан персонаж: {character.name}")
        else:
            print(f"Персонаж уже существует: {character.name}")
    
    return Character.objects.all()

def main():
    """Основная функция"""
    print("Добавление тестовых данных в базу данных Star Wars Encyclopedia...")
    print("=" * 60)
    
    # Добавляем планеты
    print("\n1. Добавление планет...")
    planets = add_planets()
    print(f"Всего планет в базе: {planets.count()}")
    
    # Добавляем персонажей
    print("\n2. Добавление персонажей...")
    characters = add_characters()
    print(f"Всего персонажей в базе: {characters.count()}")
    
    print("\n" + "=" * 60)
    print("Добавление данных завершено!")
    print(f"Планет: {planets.count()}")
    print(f"Персонажей: {characters.count()}")

if __name__ == '__main__':
    main()
