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
    description = models.TextField(blank=True, verbose_name="Описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Публикация")

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

    objects = models.Manager()
    published = PublishedPlanetManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('planet_detail', kwargs={'planet_slug': self.slug})