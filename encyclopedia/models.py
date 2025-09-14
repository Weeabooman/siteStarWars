from django.db import models

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя персонажа")
    species = models.CharField(max_length=50, blank=True, verbose_name="Вид")
    homeworld = models.ForeignKey(
        'Planet', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='residents',
        verbose_name="Родная планета"
    )
    affiliation = models.CharField(max_length=100, blank=True, verbose_name="Аффилиация/Фракция")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

class Planet(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название планеты")
    system = models.CharField(max_length=100, blank=True, verbose_name="Система/Сектор")
    description = models.TextField(blank=True, verbose_name="Описание")
    population = models.PositiveBigIntegerField(null=True, blank=True, verbose_name="Население")
    climate = models.CharField(max_length=50, blank=True, verbose_name="Климат")

    def __str__(self):
        return self.name