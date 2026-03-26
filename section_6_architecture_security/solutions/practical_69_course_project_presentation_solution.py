"""
Решение практической работы 69: Подготовка презентации курсового проекта

Этот файл содержит шаблон и рекомендации по созданию эффективной 
презентации для защиты курсового проекта.
"""

import os
from datetime import datetime


class CourseProjectPresentation:
    """Класс для управления презентацией курсового проекта"""
    
    def __init__(self, project_title, author_name, date=None):
        self.project_title = project_title
        self.author_name = author_name
        self.date = date or datetime.now().strftime("%d.%m.%Y")
        self.slides = []
        
    def add_title_slide(self):
        """Добавить титульный слайд"""
        slide = {
            "type": "title",
            "title": self.project_title,
            "subtitle": f"Автор: {self.author_name}",
            "date": self.date
        }
        self.slides.append(slide)
        return slide
        
    def add_problem_slide(self, problem_statement, relevance):
        """Добавить слайд с актуальностью и целями проекта"""
        slide = {
            "type": "problem",
            "problem": problem_statement,
            "relevance": relevance
        }
        self.slides.append(slide)
        return slide
        
    def add_architecture_slide(self, architecture_description, diagram_path=None):
        """Добавить слайд с архитектурой приложения"""
        slide = {
            "type": "architecture",
            "description": architecture_description,
            "diagram": diagram_path
        }
        self.slides.append(slide)
        return slide
        
    def add_functionality_slide(self, features):
        """Добавить слайд с реализованным функционалом"""
        slide = {
            "type": "functionality",
            "features": features
        }
        self.slides.append(slide)
        return slide
        
    def add_technologies_slide(self, technologies):
        """Добавить слайд с использованными технологиями"""
        slide = {
            "type": "technologies",
            "technologies": technologies
        }
        self.slides.append(slide)
        return slide
        
    def add_challenges_slide(self, challenges_and_solutions):
        """Добавить слайд с проблемами и их решениями"""
        slide = {
            "type": "challenges",
            "challenges": challenges_and_solutions
        }
        self.slides.append(slide)
        return slide
        
    def add_demo_slide(self, demo_steps):
        """Добавить слайд с демонстрацией"""
        slide = {
            "type": "demo",
            "steps": demo_steps
        }
        self.slides.append(slide)
        return slide
        
    def add_conclusion_slide(self, conclusions, future_work):
        """Добавить слайд с выводами"""
        slide = {
            "type": "conclusion",
            "conclusions": conclusions,
            "future_work": future_work
        }
        self.slides.append(slide)
        return slide
        
    def generate_markdown(self):
        """Сгенерировать презентацию в формате Markdown"""
        md_content = f"# {self.project_title}\n\n"
        md_content += f"**Автор:** {self.author_name}\n"
        md_content += f"**Дата:** {self.date}\n\n---\n\n"
        
        for i, slide in enumerate(self.slides, 1):
            md_content += f"## Слайд {i}: {slide['type'].title()}\n\n"
            
            if slide["type"] == "title":
                md_content += f"- **Проект:** {slide['title']}\n"
                md_content += f"- **Подзаголовок:** {slide['subtitle']}\n"
                md_content += f"- **Дата:** {slide['date']}\n"
                
            elif slide["type"] == "problem":
                md_content += f"- **Проблема:** {slide['problem']}\n"
                md_content += f"- **Актуальность:** {slide['relevance']}\n"
                
            elif slide["type"] == "architecture":
                md_content += f"{slide['description']}\n"
                if slide.get("diagram"):
                    md_content += f"\n![Диаграмма архитектуры]({slide['diagram']})\n"
                    
            elif slide["type"] == "functionality":
                md_content += "**Реализованный функционал:**\n"
                for feature in slide["features"]:
                    md_content += f"- {feature}\n"
                    
            elif slide["type"] == "technologies":
                md_content += "**Использованные технологии:**\n"
                for tech in slide["technologies"]:
                    md_content += f"- {tech}\n"
                    
            elif slide["type"] == "challenges":
                md_content += "**Проблемы и решения:**\n"
                for challenge, solution in slide["challenges"].items():
                    md_content += f"- **{challenge}:** {solution}\n"
                    
            elif slide["type"] == "demo":
                md_content += "**План демонстрации:**\n"
                for step in slide["steps"]:
                    md_content += f"- {step}\n"
                    
            elif slide["type"] == "conclusion":
                md_content += "**Выводы:**\n"
                for conclusion in slide["conclusions"]:
                    md_content += f"- {conclusion}\n"
                md_content += "\n**Перспективы развития:**\n"
                for work in slide["future_work"]:
                    md_content += f"- {work}\n"
            
            md_content += "\n---\n\n"
            
        return md_content
        
    def save_presentation(self, filename="presentation.md"):
        """Сохранить презентацию в файл"""
        content = self.generate_markdown()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename


def create_sample_presentation():
    """Создать пример презентации"""
    presentation = CourseProjectPresentation(
        project_title="Система управления задачами",
        author_name="Иванов Иван Иванович"
    )
    
    # Титульный слайд
    presentation.add_title_slide()
    
    # Актуальность
    presentation.add_problem_slide(
        problem_statement="Отсутствие удобного инструмента для персонального планирования задач",
        relevance="Актуальность заключается в необходимости эффективного управления временем и задачами"
    )
    
    # Архитектура
    presentation.add_architecture_slide(
        architecture_description="Трёхуровневая архитектура: Presentation Layer (GUI) → Business Logic Layer → Data Access Layer (SQLite)"
    )
    
    # Функционал
    presentation.add_functionality_slide([
        "Создание, редактирование и удаление задач",
        "Категоризация задач по проектам",
        "Установка сроков и приоритетов",
        "Уведомления о приближающихся сроках",
        "Экспорт задач в различные форматы"
    ])
    
    # Технологии
    presentation.add_technologies_slide([
        "Python 3.x",
        "Tkinter (GUI)",
        "SQLite (база данных)",
        "SQLAlchemy (ORM)",
        "Git (контроль версий)"
    ])
    
    # Проблемы и решения
    presentation.add_challenges_slide({
        "Сложность работы с датами": "Использование библиотеки datetime",
        "Синхронизация данных": "Внедрение паттерна Repository",
        "Тестирование": "Использование unittest и mock-объектов"
    })
    
    # Демонстрация
    presentation.add_demo_slide([
        "Показать главное окно приложения",
        "Создать новую задачу",
        "Редактировать задачу",
        "Отметить задачу как выполненную",
        "Показать фильтрацию по проектам"
    ])
    
    # Выводы
    presentation.add_conclusion_slide(
        conclusions=[
            "Разработано полнофункциональное приложение",
            "Освоены принципы ООП и паттерны проектирования",
            "Получены навыки работы с базами данных"
        ],
        future_work=[
            "Добавить синхронизацию с облачными сервисами",
            "Реализовать мобильное приложение",
            "Добавить совместную работу над задачами"
        ]
    )
    
    return presentation


# Пример использования
if __name__ == "__main__":
    # Создание примера презентации
    pres = create_sample_presentation()
    
    # Сохранение в файл
    filename = pres.save_presentation("course_project_presentation.md")
    print(f"Презентация сохранена в файл: {filename}")
    
    # Также можно получить Markdown напрямую
    # print(pres.generate_markdown())


# Рекомендации по оформлению презентации
RECOMMENDATIONS = """
# Рекомендации по созданию презентации для защиты курсового проекта

## Общие требования

1. **Объём презентации:** 10-15 слайдов
2. **Время выступления:** 7-10 минут
3. **Стиль:** лаконичный, профессиональный

## Структура презентации

### 1. Титульный слайд (1 слайд)
- Название проекта
- ФИО студента
- Название учебного заведения
- Год

### 2. Актуальность (1-2 слайда)
- Проблема, которую решает проект
- Актуальность разработки
- Цели и задачи

### 3. Архитектура (1-2 слайда)
- Структурная схема
- Основные компоненты
- Технологический стек

### 4. Функционал (2-3 слайда)
- Основные возможности
- Пользовательский интерфейс (скриншоты)
- Особенности реализации

### 5. Технологии (1 слайд)
- Использованные инструменты
- Библиотеки и фреймворки

### 6. Проблемы и решения (1 слайд)
- Сложности при разработке
- Пути их преодоления

### 7. Демонстрация (2-3 слайда)
- Ключевые сценарии использования
- Скриншоты работы

### 8. Выводы (1 слайд)
- Результаты работы
- Приобретённые навыки
- Перспективы развития

## Советы по выступлению

1. Репетируйте заранее
2. Говорите чётко и уверенно
3. Смотрите на аудиторию
4. Будьте готовы к вопросам
5. Не читайте со слайдов
6. Используйте таймер

## Оформление

- Единый стиль оформления
- Контрастные цвета
- Читаемый шрифт (не менее 24pt)
- Минимум текста на слайде
- Наглядные иллюстрации
"""
