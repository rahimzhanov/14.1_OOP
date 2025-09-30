import pytest
from src.models import Product, Category


class TestProduct:
    """Тесты для класса Product."""

    def test_product_creation(self):
        """Тест создания продукта."""
        product = Product("Телефон", "Смартфон", 999.99, 10)
        assert product.name == "Телефон"
        assert product.price == 999.99
        assert product.quantity == 10

    def test_new_product_class_method(self):
        """Тест создания продукта через класс-метод."""
        product_data = {
            'name': 'Телефон',
            'description': 'Смартфон',
            'price': 500.0,
            'quantity': 8
        }
        product = Product.new_product(product_data)
        assert isinstance(product, Product)
        assert product.name == 'Телефон'

    def test_price_validation(self):
        """Тест валидации цены."""
        product = Product("Товар", "Описание", 100.0, 5)

        # Попытка установить невалидную цену
        product.price = -50
        assert product.price == 100.0  # Цена не изменилась

        # Установка валидной цены
        product.price = 150.0
        assert product.price == 150.0

    def test_str_representation(self):
        """Тест строкового представления."""
        product = Product("Телефон", "Смартфон", 999.99, 10)
        assert str(product) == "Телефон, 999.99 руб. Остаток: 10 шт."


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_creation(self):
        """Тест создания категории."""
        product = Product("Товар", "Описание", 100.0, 5)
        category = Category("Электроника", "Техника", [product])

        assert category.name == "Электроника"
        assert "Товар, 100.0 руб. Остаток: 5 шт." in category.products

    def test_add_product(self):
        """Тест добавления товара в категорию."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 150.0, 3)

        category.add_product(product)
        assert len(category) == 1
        assert "Товар, 150.0 руб. Остаток: 3 шт." in category.products

    def test_counters(self):
        """Тест счетчиков категорий и товаров."""
        product1 = Product("Т1", "Оп1", 100.0, 1)
        product2 = Product("Т2", "Оп2", 200.0, 2)

        category1 = Category("Кат1", "Описание1", [product1])
        category2 = Category("Кат2", "Описание2", [product2])

        assert Category.category_count == 2
        assert Category.product_count == 2

    def test_private_products_access(self):
        """Тест приватности атрибута продуктов."""
        category = Category("Категория", "Описание")
        with pytest.raises(AttributeError):
            _ = category.__products
