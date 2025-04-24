from django.db import models
from django.conf import settings
from users.models import Tendency, Activity, Personality, PersonalityRecommendation
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории')
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
    def __str__(self):
        return self.name


class Test(models.Model):
    preview = models.ImageField(verbose_name='Превью', null=True, blank=True, upload_to='tests/')
    illustration = models.ImageField(verbose_name='Иллюстрация', null=True, blank=True, upload_to='tests/')
    name = models.CharField(verbose_name='Название теста')
    category = models.ForeignKey(to=Category, verbose_name='Категория', on_delete=models.CASCADE)
    trial = models.BooleanField(verbose_name='Пробное тестирование', default=False)
    description = models.TextField(verbose_name='Описание')
    
    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.trial:
            if Test.objects.filter(trial=True).exclude(pk=self.pk).exists():
                raise ValidationError("Можно создать только один пробный тест.")
        super().save(*args, **kwargs)
    

class Result(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='results') 
    text = models.TextField(verbose_name='Текст результата')
    max_score = models.PositiveIntegerField(verbose_name='Максимальный результат')
    min_score = models.PositiveIntegerField(verbose_name='Минимальный результат')
    personality_recommendations = models.ForeignKey(
        to=PersonalityRecommendation, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Персональные рекомендации',
        related_name='results',
    )
    types_activities = models.ManyToManyField(
        verbose_name="Рекомендованные виды деятельности", 
        to=Activity, 
        blank=True,
        related_name="results"
    )
    personality_type = models.ForeignKey(
        to=Personality,
        on_delete=models.CASCADE,
        verbose_name="Тип личности для результата"
    )
    tendencies = models.ManyToManyField(
        to=Tendency,
        verbose_name="Склонности для результата",
        blank=True,
        related_name="results"
    )
    

class Status(models.Model):
    name = models.CharField(verbose_name='Название статуса')


class AssigningTest(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь',
        related_name='assigned_tests',
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        verbose_name='Кем назначен',
        related_name='authored_assignments',
    )
    created_at = models.DateTimeField(verbose_name='Дата назначения', auto_now_add=True)
    due_datetime = models.DateTimeField(verbose_name='Срок выполнения', blank=True, null=True)
    status = models.ForeignKey(to=Status, on_delete=models.CASCADE, verbose_name='Статус')
    

class TestResult(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    result = models.ForeignKey(to=Result, on_delete=models.CASCADE, verbose_name='Результат')
    scores = models.IntegerField(verbose_name='Сумма баллов')
    created_at = models.DateTimeField(verbose_name='Дата окончания', auto_now_add=True)
    

class QuestionType(models.Model):
    name = models.CharField(verbose_name='Название типа')
    
    class Meta:
        verbose_name = "Тип вопроса"
        verbose_name_plural = "Типы вопроса"
        
    def __str__(self):
        return self.name
    

class Question(models.Model):
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, verbose_name='Тест')
    type = models.ForeignKey(to=QuestionType, on_delete=models.CASCADE, verbose_name='Тип')
    order = models.PositiveIntegerField(verbose_name='Порядок', null=True)
    text = models.TextField(verbose_name='Текст вопроса')
    
    class Meta:
        ordering = ['order']
    

class Variant(models.Model):
    text = models.TextField(verbose_name='Текст варианта вопроса')
    scores = models.PositiveIntegerField(verbose_name='Количество баллов')
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, verbose_name='Вопрос') 
