import pytest
from src.models import Product, Category


class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product"""
        product = Product(
            name="Телефон",
            description="Смартфон последней модели",
            price=999.99,
            quantity=10
        )

        assert product.name == "Телефон"
        assert product.description == "Смартфон последней модели"
        assert product.price == 999.99
        assert product.quantity == 10

    def test_product_attributes_types(self):
        """Тест типов атрибутов Product"""
        product = Product("Ноутбук", "Игровой ноутбук", 1500.0, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        # Создаем товары для категории
        product1 = Product("Товар1", "Описание1", 100.0, 5)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        category = Category(
            name="Электроника",
            description="Электронные товары",
            products=[product1, product2]
        )

        assert category.name == "Электроника"
        assert category.description == "Электронные товары"
        assert len(category.products) == 2
        assert isinstance(category.products[0], Product)
        assert isinstance(category.products[1], Product)

    def test_category_count_increment(self):
        """Тест подсчета количества категорий"""
        # Проверяем начальное значение
        assert Category.category_count == 0

        # Создаем первую категорию
        Category("Кат1", "Описание1", [])
        assert Category.category_count == 1

        # Создаем вторую категорию
        Category("Кат2", "Описание2", [])
        assert Category.category_count == 2

        # Создаем третью категорию
        Category("Кат3", "Описание3", [])
        assert Category.category_count == 3

    def test_product_count_increment(self):
        """Тест подсчета количества товаров"""
        # Проверяем начальное значение
        assert Category.product_count == 0

        # Создаем товары
        product1 = Product("Т1", "Оп1", 100.0, 1)
        product2 = Product("Т2", "Оп2", 200.0, 2)
        product3 = Product("Т3", "Оп3", 300.0, 3)

        # Создаем категорию с 2 товарами
        Category("Кат1", "Описание1", [product1, product2])
        assert Category.product_count == 2

        # Создаем категорию с 1 товаром
        Category("Кат2", "Описание2", [product3])
        assert Category.product_count == 3

    def test_category_with_empty_products(self):
        """Тест категории с пустым списком товаров"""
        category = Category("Пустая", "Категория без товаров", [])

        assert category.name == "Пустая"
        assert category.description == "Категория без товаров"
        assert category.products == []
        assert Category.category_count == 1
        assert Category.product_count == 0

    def test_category_with_single_product(self):
        """Тест категории с одним товаром"""
        product = Product("Единственный", "Товар", 50.0, 1)
        category = Category("Одиночная", "Один товар", [product])

        assert len(category.products) == 1
        assert category.products[0].name == "Единственный"
        assert Category.product_count == 1

    @pytest.fixture
    def sample_products(self):
        """Фикстура с примером товаров"""
        return [
            Product("Продукт A", "Описание A", 100.0, 5),
            Product("Продукт B", "Описание B", 200.0, 3),
            Product("Продукт C", "Описание C", 300.0, 7)
        ]

    def test_category_with_fixture_products(self, sample_products):
        """Тест категории с товарами из фикстуры"""
        category = Category("Тестовая", "Категория с фикстурой", sample_products)

        assert len(category.products) == 3
        assert category.products[0].name == "Продукт A"
        assert category.products[1].price == 200.0
        assert category.products[2].quantity == 7
        assert Category.product_count == 3
