"""
Упражнения к практической работе 36: Django - основы

Выполните следующие упражнения для закрепления основ Django.
"""

# Упражнение 1: Создание проекта
def exercise_create_project():
    """
    Создайте Django проект.
    """
    # Команды для создания проекта:
    # django-admin startproject myproject
    # cd myproject
    # python manage.py startapp main
    pass


# Упражнение 2: Модели Django
def exercise_models():
    """
    Создайте модели в Django.
    """
    # models.py
    from django.db import models
    
    class Article(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        published_date = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            return self.title


# Упражнение 3: URLs и Views
def exercise_urls_views():
    """
    Настройте URLs и Views в Django.
    """
    # views.py
    from django.http import HttpResponse
    
    def index(request):
        return HttpResponse("Главная страница")
    
    # urls.py
    # urlpatterns = [
    #     path('', views.index, name='index'),
    # ]


# Упражнение 4: Admin интерфейс
def exercise_admin():
    """
    Настройте Django Admin.
    """
    # admin.py
    from django.contrib import admin
    from .models import Article
    
    @admin.register(Article)
    class ArticleAdmin(admin.ModelAdmin):
        list_display = ('title', 'published_date')


if __name__ == "__main__":
    print("Упражнения для изучения Django")
