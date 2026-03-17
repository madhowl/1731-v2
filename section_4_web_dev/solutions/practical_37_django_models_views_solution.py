# -*- coding: utf-8 -*-
"""
Практическое занятие 37: Django - модели и представления
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по моделям и представлениям в Django.

Примечание: Для запуска этого кода требуется Django проект.
"""

# ============================================================================
# Упражнение 1: Модели в Django
# ============================================================================

# Пример моделей Django

MODELS_EXAMPLE = '''
# blog/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime


class Category(models.Model):
    """Модель категории статей"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL-адрес')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """Модель статьи блога"""
    
    # Выбор статуса публикации
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'
        ARCHIVED = 'archived', 'В архиве'
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-адрес')
    content = models.TextField(verbose_name='Содержание')
    excerpt = models.CharField(max_length=300, blank=True, verbose_name='Краткое описание')
    
    # Связь с автором (Foreign Key)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Автор'
    )
    
    # Связь с категорией
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name='Категория'
    )
    
    # Связь многие-ко-многим с тегами
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        verbose_name='Теги'
    )
    
    # Изображение
    image = models.ImageField(
        upload_to='articles/%Y/%m/%d/',
        blank=True,
        verbose_name='Изображение'
    )
    
    # Статус и даты
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус'
    )
    view_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемая')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = datetime.now()
        
        super().save(*args, **kwargs)
    
    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    """Модель комментария к статье"""
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Статья'
    )
    
    author_name = models.CharField(max_length=100, verbose_name='Имя')
    author_email = models.EmailField(verbose_name='Email')
    author_ip = models.GenericIPAddressField(null=True, blank=True)
    
    content = models.TextField(verbose_name='Комментарий')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    is_spam = models.BooleanField(default=False, verbose_name='Спам')
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Комментарий от {self.author_name} к {self.article.title}"
'''


# ============================================================================
# Упражнение 2: Django ORM и запросы
# ============================================================================

DJANGO_ORM_EXAMPLES = '''
# Примеры запросов к базе данных с использованием Django ORM

from django.contrib.auth.models import User
from blog.models import Article, Category, Tag, Comment


# === СОЗДАНИЕ (Create) ===

# Создание категории
category = Category.objects.create(
    name='Программирование',
    description='Статьи о программировании'
)

# Создание статьи
article = Article.objects.create(
    title='Введение в Python',
    slug='introduction-to-python',
    content='Полный текст статьи...',
    author=user,  # Объект пользователя
    category=category,
    status=Article.Status.PUBLISHED
)

# Добавление тегов
tag1 = Tag.objects.get_or_create(name='Python', slug='python')[0]
tag2 = Tag.objects.get_or_create(name='Программирование', slug='programming')[0]
article.tags.add(tag1, tag2)

# Создание с проверкой
category, created = Category.objects.get_or_create(
    name='Веб-разработка',
    defaults={'description': 'Статьи о веб-разработке'}
)


# === ЧТЕНИЕ (Read) ===

# Получение всех опубликованных статей
articles = Article.objects.filter(status=Article.Status.PUBLISHED)

# Получение одной статьи по slug
article = Article.objects.get(slug='introduction-to-python')

# Получение статьи с обработкой исключения
from django.shortcuts import get_object_or_404
article = get_object_or_404(Article, slug='introduction-to-python')

# Связанные запросы
author_articles = Article.objects.filter(author=author)
category_articles = Article.objects.filter(category=category)

# Теги статьи
article_tags = article.tags.all()

# Комментарии статьи
article_comments = article.comments.filter(is_approved=True)


# === ОБНОВЛЕНИЕ (Update) ===

# Обновление одной записи
article.title = 'Новое название'
article.save()

# Обновление с использованием update()
Article.objects.filter(status=Article.Status.DRAFT).update(
    status=Article.Status.ARCHIVED
)

# Увеличение счётчика просмотров
Article.objects.filter(pk=article.pk).update(
    view_count=models.F('view_count') + 1
)


# === УДАЛЕНИЕ (Delete) ===

# Удаление одной записи
article.delete()

# Массовое удаление
Article.objects.filter(status=Article.Status.ARCHIVED).delete()


# === ФИЛЬТРАЦИЯ ===

# Простая фильтрация
Article.objects.filter(status=Article.Status.PUBLISHED)
Article.objects.filter(category__name='Программирование')

# Исключение
Article.objects.exclude(status=Article.Status.ARCHIVED)

# Сложные условия с Q
from django.db.models import Q

Article.objects.filter(
    Q(title__icontains='python') | Q(content__icontains='python')
)

Article.objects.filter(
    Q(status=Article.Status.PUBLISHED) &
    (Q(category__slug='programming') | Q(tags__slug='python'))
).distinct()


# === СОРТИРОВКА ===

# По возрастанию
articles = Article.objects.order_by('title')

# По убыванию
articles = Article.objects.order_by('-created_at')

# Несколько полей
articles = Article.objects.order_by('-is_featured', '-created_at')


# === ПАГИНАЦИЯ ===

from django.core.paginator import Paginator

articles = Article.objects.all()
paginator = Paginator(articles, 10)  # 10 статей на странице
page = paginator.get_page(1)


# === АГРЕГАЦИЯ ===

from django.db.models import Count, Avg, Sum, Max, Min, Q

# Количество статей
count = Article.objects.count()

# Количество статей у автора
author_article_count = Article.objects.filter(author=author).count()

# Среднее значение
avg_views = Article.objects.aggregate(avg_views=Avg('view_count'))

# Группировка
categories_with_articles = Category.objects.annotate(
    article_count=Count('articles')
).filter(article_count__gt=0)


# === ВЫБОРКА ПОЛЕЙ (Select) ===

# Выборка только нужных полей
articles = Article.objects.only('title', 'slug', 'created_at')

# Выборка с исключением
articles = Article.objects.defer('content')

# Выборка связанных объектов
articles = Article.objects.prefetch_related('tags', 'category', 'author')
articles = Article.objects.select_related('category', 'author')


# === RAW SQL ===

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM blog_article WHERE id = %s", [article_id])
    row = cursor.fetchone()
'''


# ============================================================================
# Упражнение 3: Функциональные представления (FBV)
# ============================================================================

FUNCTIONAL_VIEWS_EXAMPLE = '''
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import F
from .models import Article, Category, Tag, Comment


def article_list(request):
    """Список всех опубликованных статей"""
    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED
    ).select_related('category', 'author')
    
    # Пагинация
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/article_list.html', {
        'page_obj': page_obj,
        'articles': page_obj.object_list,
    })


def article_detail(request, slug):
    """Детальная страница статьи"""
    article = get_object_or_404(
        Article.objects.select_related('category', 'author'),
        slug=slug,
        status=Article.Status.PUBLISHED
    )
    
    # Увеличение счётчика просмотров
    Article.objects.filter(pk=article.pk).update(view_count=F('view_count') + 1)
    
    # Комментарии
    comments = article.comments.filter(
        is_approved=True,
        parent__isnull=True
    ).select_related('author')
    
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
    })


def category_articles(request, slug):
    """Статьи категории"""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        category=category,
        status=Article.Status.PUBLISHED
    )
    
    return render(request, 'blog/category.html', {
        'category': category,
        'articles': articles,
    })


def tag_articles(request, slug):
    """Статьи по тегу"""
    tag = get_object_or_404(Tag, slug=slug)
    articles = tag.articles.filter(status=Article.Status.PUBLISHED)
    
    return render(request, 'blog/tag.html', {
        'tag': tag,
        'articles': articles,
    })


@login_required
def create_article(request):
    """Создание новой статьи"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        
        article = Article.objects.create(
            title=title,
            slug=title.lower().replace(' ', '-'),
            content=content,
            category_id=category_id,
            author=request.user,
            status=Article.Status.DRAFT
        )
        
        messages.success(request, 'Статья создана!')
        return redirect('blog:article_detail', slug=article.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog/create_article.html', {
        'categories': categories,
    })


@login_required
def edit_article(request, article_id):
    """Редактирование статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверка авторства
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для редактирования этой статьи')
        return redirect('blog:article_detail', slug=article.slug)
    
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.category_id = request.POST.get('category')
        article.save()
        
        messages.success(request, 'Статья обновлена!')
        return redirect('blog:article_detail', slug=article.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog/edit_article.html', {
        'article': article,
        'categories': categories,
    })


@login_required
def delete_article(request, article_id):
    """Удаление статьи"""
    article = get_object_or_404(Article, id=article_id)
    
    # Проверка авторства
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для удаления этой статьи')
        return redirect('blog:article_detail', slug=article.slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена!')
        return redirect('blog:article_list')
    
    return render(request, 'blog/delete_article.html', {'article': article})


@require_http_methods(["POST"])
def add_comment(request, article_id):
    """Добавление комментария"""
    article = get_object_or_404(Article, id=article_id)
    
    author_name = request.POST.get('author_name')
    author_email = request.POST.get('author_email')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent')
    
    comment = Comment.objects.create(
        article=article,
        author_name=author_name,
        author_email=author_email,
        content=content,
        parent_id=parent_id if parent_id else None,
        is_approved=True  # Или False для модерации
    )
    
    messages.success(request, 'Комментарий добавлен!')
    return redirect('blog:article_detail', slug=article.slug)
'''


# ============================================================================
# Упражнение 4: Классовые представления (CBV)
# ============================================================================

CLASS_BASED_VIEWS_EXAMPLE = '''
# blog/views.py (продолжение)

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, RedirectView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Article


class ArticleListView(ListView):
    """Список статей"""
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        return Article.objects.filter(
            status=Article.Status.PUBLISHED
        ).select_related('category', 'author')


class ArticleDetailView(DetailView):
    """Детальная страница статьи"""
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    
    def get_queryset(self):
        return Article.objects.filter(
            status=Article.Status.PUBLISHED
        ).select_related('category', 'author').prefetch_related('tags')
    
    def get_object(self, queryset=None):
        article = super().get_object(queryset)
        # Увеличение счётчика просмотров
        Article.objects.filter(pk=article.pk).update(
            view_count=models.F('view_count') + 1
        )
        return article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание статьи"""
    model = Article
    template_name = 'blog/article_form.html'
    fields = ['title', 'content', 'category', 'tags', 'image']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Статья создана!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.object.slug})


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование статьи"""
    model = Article
    template_name = 'blog/article_form.html'
    fields = ['title', 'content', 'category', 'tags', 'image', 'status']
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Статья обновлена!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.object.slug})


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление статьи"""
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:article_list')
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Статья удалена!')
        return super().delete(request, *args, **kwargs)


# URL-конфигурация для CBV
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
'''


# ============================================================================
# Упражнение 5: Формы в Django
# ============================================================================

DJANGO_FORMS_EXAMPLE = '''
# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    """Форма для создания и редактирования статьи"""
    
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'excerpt', 'category', 'tags', 'image', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            from django.utils.text import slugify
            slug = slugify(self.cleaned_data.get('title', ''))
        
        # Проверка уникальности slug
        qs = Article.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise forms.ValidationError('URL-адрес уже используется')
        
        return slug


class CommentForm(forms.ModelForm):
    """Форма для комментария"""
    
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Комментарий'
            }),
        }


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
        
        return user
'''


# ============================================================================
# Упражнение 6: Admin-интерфейс
# ============================================================================

DJANGO_ADMIN_EXAMPLE = '''
# blog/admin.py

from django.contrib import admin
from .models import Category, Tag, Article, Comment
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Статей'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Статей'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'is_featured', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'tags']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Метаданные', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Публикация', {
            'fields': ('status', 'is_featured', 'published_at', 'view_count')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.status == Article.Status.PUBLISHED and not obj.published_at:
            from datetime import datetime
            obj.published_at = datetime.now()
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['is_approved', 'is_spam', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_comments', 'disapprove_comments', 'mark_as_spam']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Одобрить комментарии'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = 'Отклонить комментарии'
    
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True)
    mark_as_spam.short_description = 'Отметить как спам'
'''


# ============================================================================
# Вывод информации
# ============================================================================

def main():
    """Вывод информации о Django моделях и представлениях"""
    print("=" * 70)
    print("Практическое занятие 37: Django - модели и представления")
    print("=" * 70)
    print()
    print("В этом файле представлены примеры:")
    print("1. Модели Django с различными типами полей")
    print("2. Django ORM - запросы к базе данных")
    print("3. Функциональные представления (FBV)")
    print("4. Классовые представления (CBV)")
    print("5. Формы в Django")
    print("6. Настройка Admin-интерфейса")
    print()
    print("=" * 70)
    print("Для запуска требуется Django проект:")
    print("1. pip install django")
    print("2. django-admin startproject myproject")
    print("3. python manage.py startapp blog")
    print("=" * 70)


if __name__ == '__main__':
    main()
