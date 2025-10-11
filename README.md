    # Product & Category Management System

Простая система для управления товарами и категориями на Python с использованием ООП.

## 🚀 Функциональность

### Класс `Product`
- **Атрибуты**: название, описание, цена, количество
- **Приватная цена** с валидацией (не может быть ≤ 0)
- **Класс-метод** `new_product()` для создания из словаря
- **Строковое представление**: "Название, 100 руб. Остаток: 5 шт."

### Класс `Category`  
- **Атрибуты**: название, описание, список товаров
- **Приватный список товаров** - доступ только через методы
- **Метод** `add_product()` для добавления товаров
- **Автоматический подсчет** категорий и товаров
- **Геттер** для красивого вывода товаров

## 📦 Установка

```bash
git clone <repository>
cd <project>
pip install -r requirements.txt
```

## 💻 Использование
### Создание товара
from src.models import Product, Category

product = Product("Телефон", "Смартфон", 999.99, 10)

### Или через класс-метод
product_data = {
    'name': 'Ноутбук', 
    'description': 'Игровой',
    'price': 1500.0,
    'quantity': 5
}
product = Product.new_product(product_data)

### Создание категории
category = Category("Электроника", "Техника")

### Добавление товара
category.add_product(product)

### Просмотр товаров
print(category.products)

## 🧪 Тестирование

### Запуск тестов
pytest tests/

### Тесты с покрытием
pytest --cov=src

### Проверка стиля кода
flake8 src tests
🛠 Технологии
Python 3.8+

pytest для тестирования

flake8 для проверки стиля

poetry для управления зависимостями

## 📁 Структура проекта
````
project/
├── src/
│   └── models.py
├── tests/
│   └── test_models.py
├── pyproject.toml
└── README.md
