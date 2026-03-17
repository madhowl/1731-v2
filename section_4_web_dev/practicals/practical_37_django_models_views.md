# Практическое занятие 37: Django - модели и представления

## Работа с моделями и представлениями в Django

### Цель занятия:
Научиться создавать модели данных в Django, использовать Django ORM для работы с базой данных, создавать представления (views) и формы, использовать административный интерфейс.

### Задачи:
1. Создавать модели данных в Django
2. Использовать Django ORM для запросов
3. Создавать представления (views)
4. Работать с формами в Django
5. Настраивать админ-панель

### План работы:
1. Создание моделей в Django
2. Django ORM и запросы
3. Представления (Function-based и Class-based)
4. Формы в Django
5. Административный интерфейс
6. Практические задания

---

## 1. Создание моделей в Django

### Пример 1: Базовая модель

```python
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
```

### Пример 2: Модель статьи с полями

```python
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
        'Tag',
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
```

### Пример 3: Модель комментария

```python
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
```

### Пример 4: Модель тега

```python
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
```

---

## 2. Django ORM и запросы

### Пример 5: Создание и сохранение объектов

```python
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
    author=author,  # Объект пользователя
    category=category,
    status=Article.Status.PUBLISHED
)

# Добавление тегов
tag1 = Tag.objects.get_or_create(name='Python', slug='python')[0]
tag2 = Tag.objects.get_or_create(name='Программирование', slug='programming')[0]
article.tags.add(tag1, tag2)

# Сохранение изменений
article.save()
```

### Пример 6: Запросы к базе данных

```python
# Получение всех опубликованных статей
articles = Article.objects.filter(status=Article.Status.PUBLISHED)

# Получение одной статьи по slug
article = Article.objects.get(slug='introduction-to-python')

# Связанные запросы
# Статьи автора
author_articles = Article.objects.filter(author=author)

# Статьи категории
category_articles = Article.objects.filter(category=category)

# Теги статьи
article_tags = article.tags.all()

# Комментарии статьи
article_comments = article.comments.filter(is_approved=True)
```

### Пример 7: Сложные запросы с Q-объектами

```python
from django.db.models import Q, Count, Prefetch

# Поиск по нескольким полям
articles = Article.objects.filter(
    Q(title__icontains='python') | Q(content__icontains='python')
)

# Исключение
articles = Article.objects.exclude(status=Article.Status.ARCHIVED)

# Сложные условия
articles = Article.objects.filter(
    Q(status=Article.Status.PUBLISHED) &
    (Q(category__slug='programming') | Q(tags__slug='python'))
).distinct()

# Агрегация
from django.db.models import Count, Avg, Sum, Max, Min

# Количество статей у автора
author_article_count = Article.objects.filter(author=author).count()

# Количество комментариев к статье
article_comment_count = Comment.objects.filter(article=article).count()

# Среднее значение
avg_views = Article.objects.aggregate(avg_views=Avg('view_count'))

# Группировка
categories_with_articles = Category.objects.annotate(
    article_count=Count('articles')
).filter(article_count__gt=0)
```

### Пример 8: Выборки (Select)

```python
# Выборка только нужных полей
articles = Article.objects.only('title', 'slug', 'created_at')

# Выборка с исключением
articles = Article.objects.defer('content')

# Выборка связанных объектов (prefetch)
articles = Article.objects.prefetch_related('tags', 'category', 'author')

# Выборка с select_related (для ForeignKey)
articles = Article.objects.select_related('category', 'author')

# Прямой SQL-запрос
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM blog_article WHERE id = %s", [article_id])
    row = cursor.fetchone()
```

---

## 3. Представления (Views)

### Пример 9: Функциональные представления

```python
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
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
    Article.objects.filter(pk=article.pk).update(view_count=models.F('view_count') + 1)
    
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
        # Обработка формы
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
        
        return redirect('blog:article_detail', slug=article.slug)
    
    categories = Category.objects.all()
    return render(request, 'blog/create_article.html', {
        'categories': categories,
    })
```

### Пример 10: Классовые представления (CBV)

```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, RedirectView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание статьи"""
    model = Article
    template_name = 'blog/article_form.html'
    fields = ['title', 'content', 'category', 'tags', 'image']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
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
        return self.request.user == article.author
    
    def get_success_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.object.slug})

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление статьи"""
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = reverse_lazy('blog:article_list')
    
    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
```

---

## 4. Формы в Django

### Пример 11: Создание формы

```python
# blog/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    """Форма для создания/редактирования статьи"""
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'image', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise ValidationError('Заголовок слишком короткий')
        return title
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 50:
            raise ValidationError('Содержание слишком короткое')
        return content

class CommentForm(forms.ModelForm):
    """Форма комментария"""
    
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
                'placeholder': 'Ваш комментарий'
            }),
        }
    
    def clean_author_email(self):
        email = self.cleaned_data['author_email']
        # Дополнительная валидация
        return email

class SearchForm(forms.Form):
    """Форма поиска"""
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск...'
        })
    )
```

### Пример 12: Использование формы в представлении

```python
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ArticleForm, CommentForm, SearchForm

def create_article(request):
    """Создание статьи с формой"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # Сохранение ManyToMany полей
            
            messages.success(request, 'Статья успешно создана!')
            return redirect('blog:article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    
    return render(request, 'blog/article_form.html', {
        'form': form,
        'action': 'Создание статьи'
    })

def add_comment(request, article_slug):
    """Добавление комментария"""
    article = get_object_or_404(Article, slug=article_slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog:article_detail', slug=article_slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/comment_form.html', {
        'form': form,
        'article': article
    })

def search(request):
    """Поиск статей"""
    form = SearchForm(request.GET)
    results = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status=Article.Status.PUBLISHED
        )
    
    return render(request, 'blog/search.html', {
        'form': form,
        'results': results,
        'query': query
    })
```

---

## 5. Административный интерфейс

### Пример 13: Настройка админ-панели

```python
# blog/admin.py

from django.contrib import admin
from .models import Category, Article, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админ-панели для категорий"""
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Настройка админ-панели для статей"""
    
    # Список статей
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    
    # Действия
    actions = ['publish_articles', 'unpublish_articles', 'mark_as_featured']
    
    # Поля в редактировании
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image')
        }),
        ('Связи', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Публикация', {
            'fields': ('status', 'is_featured', 'published_at', 'created_at', 'updated_at')
        }),
        ('Статистика', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    ordering = ['-published_at']
    
    @admin.action(description='Опубликовать выбранные статьи')
    def publish_articles(self, request, queryset):
        queryset.update(status=Article.Status.PUBLISHED)
    
    @admin.action(description='Снять с публикации')
    def unpublish_articles(self, request, queryset):
        queryset.update(status=Article.Status.DRAFT)
    
    @admin.action(description='Отметить как рекомендуемые')
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['is_approved', 'is_spam', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_comments', 'mark_as_spam']
    
    @admin.action(description='Одобрить комментарии')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    
    @admin.action(description='Отметить как спам')
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True)
```

---

## 6. Практические задания

### Задание 1: Модель товара
Создайте модель Product для интернет-магазина:
- Название, описание, цена
- Категория, производитель
- Изображение, остаток на складе
- Дата создания и обновления

### Задание 2: CRUD для товаров
Создайте полный CRUD для товаров:
- Список товаров с пагинацией
- Детальная страница товара
- Создание/редактирование/удаление

### Задание 3: Форма заказа
Создайте модель и форму для заказа:
- Order: товары, количество, клиент, статус, дата
- Связь many-to-many с товарами

### Задание 4: Админ-панель
Настройте полноценную админ-панель для управления товарами и заказами.

### Задание 5: Фильтрация
Добавьте фильтрацию товаров по категории, цене, производителю.

---

## Дополнительные задания

### Задание 6: Система рейтингов
Добавьте возможность оценивать статьи/товары.

### Задание 7: Избранное
Реализуйте функционал избранного для пользователей.

### Задание 8: Уведомления
Создайте систему уведомлений о новых комментариях/заказах.

---

## Контрольные вопросы:
1. Как создать модель в Django?
2. Какие типы полей вы знаете?
3. Как создать связь один-ко-многим?
4. Как создать связь многие-ко-многим?
5. Что такое ORM и как её использовать?
6. Чем отличаются функциональные представления от классовых?
7. Как создать форму в Django?
8. Как настроить админ-панель?
