from django.db import models
from django.urls import reverse

# Create your models here.

class PublishedCharacterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Character.Status.PUBLISHED)

class PublishedPlanetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Planet.Status.PUBLISHED)

class Character(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=100, unique=True, verbose_name="Имя персонажа")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True, blank=True, verbose_name="URL")
    species = models.CharField(max_length=50, blank=True, verbose_name="Вид")
    homeworld = models.ForeignKey(
        'Planet', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='residents',
        verbose_name="Родная планета"
    )
    affiliation = models.CharField(max_length=100, blank=True, verbose_name="Фракция")
    # Новая связь один-ко-многим (многие персонажи к одной фракции)
    faction = models.ForeignKey(
        'Faction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name="Фракция (модель)"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Публикация")
    # Связь многие-ко-многим: теги персонажа
    tags = models.ManyToManyField('Tag', related_name='characters', blank=True, verbose_name="Теги")

    objects = models.Manager()
    published = PublishedCharacterManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('character_detail', kwargs={'character_slug': self.slug})

class Planet(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=100, unique=True, verbose_name="Название планеты")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True, blank=True, verbose_name="URL")
    system = models.CharField(max_length=100, blank=True, verbose_name="Система/Сектор")
    description = models.TextField(blank=True, verbose_name="Описание")
    population = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Население")
    climate = models.CharField(max_length=50, blank=True, verbose_name="Климат")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Публикация")
    # Теги для планет (многие-ко-многим)
    tags = models.ManyToManyField('Tag', related_name='planets', blank=True, verbose_name="Теги")

    objects = models.Manager()
    published = PublishedPlanetManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('planet_detail', kwargs={'planet_slug': self.slug})

# Модель фракции (один-ко-многим с персонажами)
class Faction(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название фракции")
    side = models.CharField(max_length=50, blank=True, verbose_name="Сторона силы")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Фракция"
        verbose_name_plural = "Фракции"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('faction_detail', kwargs={'faction_slug': self.slug})

# Модель тегов (многие-ко-многим с персонажами и планетами)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=60, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'tag_slug': self.slug})

# OneToOne подробности персонажа
class CharacterDetail(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='detail', verbose_name="Персонаж")
    lightsaber_color = models.CharField(max_length=30, blank=True, verbose_name="Цвет светового меча")
    birth_year = models.CharField(max_length=20, blank=True, verbose_name="Год рождения")
    midichlorians = models.PositiveIntegerField(null=True, blank=True, verbose_name="Мидихлорианы")

    class Meta:
        verbose_name = "Детали персонажа"
        verbose_name_plural = "Детали персонажей"

    def __str__(self):
        return f"Детали: {self.character.name}"