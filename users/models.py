from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Role(models.Model):
    name = models.CharField(verbose_name='Название роли')
    
    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
    
    def __str__(self):
        return self.name
    

class UserGroup(models.Model):
    name = models.CharField(verbose_name='Название группы')
    
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
    
    def __str__(self):
        return self.name
    
class PersonalityRecommendation(models.Model):
    text = models.TextField(verbose_name='Текст')
    
    class Meta:
        verbose_name = "Персональные рекомендации"
        verbose_name_plural = "Персональные рекомендации"
        
    def __str__(self):
        return self.text[:30] + '...'

    
class Activity(models.Model):
    name = models.CharField(verbose_name='Название деятельности')
    description = models.TextField(verbose_name='Описание')
    
    class Meta:
        verbose_name = "Вид деятельности"
        verbose_name_plural = "Виды деятельности"
        
    def __str__(self):
        return self.name


class Personality(models.Model):
    name = models.CharField(verbose_name='Название личности')
    recommendations = models.TextField(verbose_name="Рекомендации для типа личности")
    
    class Meta:
        verbose_name = "Тип личности"
        verbose_name_plural = "Типы личности"
        
    def __str__(self):
        return self.name
    
    
class Tendency(models.Model):
    name = models.CharField(verbose_name='Название склонности')
    
    class Meta:
        verbose_name = "Склонность"
        verbose_name_plural = "Склонности"
        
    def __str__(self):
        return self.name
    
    
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Поле "Логин" обязательно.')

        username = self.model.normalize_username(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.objects.get_or_create(name='админ')[0])
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, password, **extra_fields)
    

class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(role__name='студент')


class User(AbstractUser):
    objects = UserManager()
    objects_students = StudentManager()
    
    patronymic = models.CharField(verbose_name="Отчество", null=True, blank=True)
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, verbose_name='Роль')
    group = models.ForeignKey(to=UserGroup, on_delete=models.CASCADE, verbose_name='Группа', null=True)
    personality_type = models.ForeignKey(blank=True, null=True, verbose_name="Тип личности", to=Personality, on_delete=models.SET_NULL)
    tendencies = models.ManyToManyField(verbose_name="Склонности", to=Tendency, blank=True, related_name="users")
    personality_recommendations = models.ManyToManyField(
        verbose_name='Персональные рекомендации', 
        to=PersonalityRecommendation,
        blank=True,
        related_name="users",
    )
    types_activities = models.ManyToManyField(
        verbose_name="Рекомендованные виды деятельности", 
        to=Activity, 
        blank=True, 
        related_name="users"
    )
    is_banned = models.BooleanField(verbose_name="Блокировка", default=False)
    
    def save(self, *args, **kwargs):
        if self.role.name.lower() == 'психолог':
            self.is_staff = True
        super().save(*args, **kwargs)
