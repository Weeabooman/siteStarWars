from django import template

# База данных категорий для Star Wars
categories_db = [
    {'id': 1, 'name': 'Джедаи'},
    {'id': 2, 'name': 'Ситхи'},
    {'id': 3, 'name': 'Повстанцы'},
    {'id': 4, 'name': 'Империя'},
    {'id': 5, 'name': 'Сенаторы'},
    {'id': 6, 'name': 'Пилоты'},
]

# База данных фракций
factions_db = [
    {'id': 1, 'name': 'Галактическая Республика'},
    {'id': 2, 'name': 'Галактическая Империя'},
    {'id': 3, 'name': 'Альянс Повстанцев'},
    {'id': 4, 'name': 'Новая Республика'},
    {'id': 5, 'name': 'Первый Орден'},
    {'id': 6, 'name': 'Сопротивление'},
]

register = template.Library()

@register.simple_tag()
def get_categories():
    """Возвращает список категорий персонажей"""
    return categories_db

@register.simple_tag()
def get_factions():
    """Возвращает список фракций"""
    return factions_db

@register.filter()
def force_side(value):
    """Определяет сторону Силы по аффилиации"""
    if not value:
        return "Неизвестно"
    
    value_lower = value.lower()
    if any(word in value_lower for word in ['джедай', 'jedi', 'республика', 'republic']):
        return "Светлая сторона"
    elif any(word in value_lower for word in ['ситх', 'sith', 'империя', 'empire']):
        return "Темная сторона"
    else:
        return "Нейтральная"

@register.filter()
def population_format(value):
    """Форматирует население планеты"""
    if not value:
        return "Неизвестно"
    
    if value >= 1000000000:
        return f"{value / 1000000000:.1f} млрд"
    elif value >= 1000000:
        return f"{value / 1000000:.1f} млн"
    elif value >= 1000:
        return f"{value / 1000:.1f} тыс"
    else:
        return str(value)
