"""
Упражнения к практической работе 37: Django - модели и представления

Выполните упражнения по работе с моделями и представлениями в Django.
"""

# Упражнение 1: Модели с связями
def exercise_related_models():
    """
    Создайте связанные модели.
    """
    from django.db import models
    
    class Category(models.Model):
        name = models.CharField(max_length=100)
    
    class Product(models.Model):
        name = models.CharField(max_length=200)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Упражнение 2: CBV (Class-Based Views)
def exercise_class_based_views():
    """
    Используйте CBV для CRUD операций.
    """
    from django.views.generic import ListView, DetailView, CreateView
    from django.urls import path
    from .models import Product
    
    class ProductListView(ListView):
        model = Product
        template_name = 'products/list.html'
        context_object_name = 'products'
    
    class ProductDetailView(DetailView):
        model = Product
        template_name = 'products/detail.html'
    
    class ProductCreateView(CreateView):
        model = Product
        fields = ['name', 'price', 'category']
        template_name = 'products/form.html'


# Упражнение 3: Миграции
def exercise_migrations():
    """
    Работа с миграциями.
    """
    # Создать миграции:
    # python manage.py makemigrations
    
    # Применить миграции:
    # python manage.py migrate
    
    # Показать SQL:
    # python manage.py sqlmigrate app_name 0001


if __name__ == "__main__":
    print("Упражнения по Django")
