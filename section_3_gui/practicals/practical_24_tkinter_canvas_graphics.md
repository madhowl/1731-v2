# Практическое занятие 24: Tkinter - Canvas и графика

## Цель занятия
Изучить возможности виджета Canvas для создания графических приложений, анимаций и интерактивных элементов в Tkinter.

## Задачи
1. Освоить базовые операции рисования на Canvas
2. Научиться создавать интерактивные элементы
3. Реализовать анимацию
4. Создать простой графический редактор
5. Разработать игру на Canvas

## Ход работы

### 1. Основы Canvas

```python
import tkinter as tk

def create_basic_canvas(parent, width=400, height=400):
    """
    Создает базовый Canvas
    
    Args:
        parent: Родительский виджет
        width: Ширина
        height: Высота
    """
    # ВАШ КОД ЗДЕСЬ - создайте Canvas и нарисуйте:
    # Линии, прямоугольники, овалы
    pass
```

---

## 1. Теоретическая часть: Canvas и графика

### Уровень 1 - Начальный

#### Задание 1.1: Основы Canvas

Изучите базовые операции с Canvas:

```python
class BasicCanvasDemo:
    """
    Демонстрация основ Canvas
    """
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()
        
        # ВАШ КОД ЗДЕСЬ - нарисуйте:
        # Линию (create_line)
        # Прямоугольник (create_rectangle)
        # Овал (create_oval)
        # Текст (create_text)
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Линия
canvas.create_line(10, 10, 100, 100, fill="red", width=3)

# Прямоугольник
canvas.create_rectangle(120, 10, 220, 110, fill="blue", outline="darkblue")

# Овал
canvas.create_oval(240, 10, 340, 110, fill="green", outline="darkgreen")

# Многоугольник
canvas.create_polygon(50, 150, 100, 200, 50, 250, fill="orange")

# Текст
canvas.create_text(200, 300, text="Привет, Canvas!", font=("Arial", 16), fill="purple")

root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Интерактивная графика

Создайте интерактивные элементы:

```python
class DraggableShape:
    """
    Перетаскиваемая фигура
    """
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        # ВАШ КОД ЗДЕСЬ - создайте фигуру и обработайте:
        # <Button-1> - начало перетаскивания
        # <B1-Motion> - перетаскивание
        # <ButtonRelease-1> - конец перетаскивания
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk

class DraggableShape:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.shape = canvas.create_rectangle(x, y, x+50, y+50, fill="blue", tags="draggable")
        
        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.shape, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.shape, "<ButtonRelease-1>", self.on_release)
        
        self.drag_data = {"x": 0, "y": 0}
        
    def on_click(self, event):
        self.drag_data = {"x": event.x, "y": event.y}
        self.canvas.itemconfig(self.shape, fill="lightblue")
        
    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.shape, dx, dy)
        self.drag_data = {"x": event.x, "y": event.y}
        
    def on_release(self, event):
        self.canvas.itemconfig(self.shape, fill="blue")

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=400, bg="white")
canvas.pack()

shape = DraggableShape(canvas, 50, 50)
shape2 = DraggableShape(canvas, 150, 150)

root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Анимация

Реализуйте анимацию:

```python
class AnimationDemo:
    """
    Демонстрация анимации
    """
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack()
        
        # ВАШ КОД ЗДЕСЬ - создайте анимацию:
        # Используйте root.after() для обновления
        pass
        
    def animate(self):
        """
        Обновляет кадр анимации
        """
        # ВАШ КОД ЗДЕСЬ - обновите позицию объекта
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
import random

class BouncingBall:
    def __init__(self, canvas):
        self.canvas = canvas
        self.radius = 20
        self.x = 200
        self.y = 150
        self.dx = 3
        self.dy = 3
        
        self.ball = canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill="red"
        )
        
    def update(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        self.x += self.dx
        self.y += self.dy
        
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.dy *= -1
            
        self.canvas.move(self.ball, self.dx, self.dy)

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

ball = BouncingBall(canvas)

def animate():
    ball.update()
    root.after(16, animate)

animate()
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Скриншоты и анимации
- Описание алгоритмов
- Оптимизация производительности

## Критерии оценки
- Функциональность: 40%
- Интерактивность: 25%
- Качество кода: 20%
- Документация: 15%
