import pytest
from src.models import Product, Category, Smartphone, LawnGrass


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

    def test_new_product_missing_fields(self):
        """Тест создания продукта с отсутствующими полями."""
        incomplete_data = {
            'name': 'Телефон',
            'description': 'Смартфон'
            # отсутствуют price и quantity
        }
        with pytest.raises(ValueError):
            Product.new_product(incomplete_data)

    def test_price_validation(self):
        """Тест валидации цены."""
        product = Product("Товар", "Описание", 100.0, 5)

        # Попытка установить невалидную цену
        product.price = -50
        assert product.price == 100.0  # Цена не изменилась

        # Установка валидной цены
        product.price = 150.0
        assert product.price == 150.0

    def test_price_validation_zero(self):
        """Тест валидации нулевой цены."""
        product = Product("Товар", "Описание", 100.0, 5)
        product.price = 0
        assert product.price == 100.0  # Цена не должна измениться

    def test_str_representation(self):
        """Тест строкового представления."""
        product = Product("Телефон", "Смартфон", 999.99, 10)
        assert str(product) == "Телефон, 999.99 руб. Остаток: 10 шт."

    def test_add_products(self):
        """Тест сложения продуктов."""
        product1 = Product("Товар1", "Описание1", 100.0, 2)  # 100 * 2 = 200
        product2 = Product("Товар2", "Описание2", 50.0, 3)  # 50 * 3 = 150

        total = product1 + product2
        assert total == 350.0  # 200 + 150

    def test_add_product_with_invalid_type(self):
        """Тест сложения продукта с неверным типом."""
        product = Product("Товар", "Описание", 100.0, 2)

        with pytest.raises(TypeError):
            product + "не продукт"

        with pytest.raises(TypeError):
            product + 123

    def test_private_price_access(self):
        """Тест приватности атрибута цены."""
        product = Product("Товар", "Описание", 100.0, 5)

        # Прямой доступ к __price должен вызывать ошибку
        with pytest.raises(AttributeError):
            _ = product.__price


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
        assert "Товар, 100.0 руб. Остаток: 5 шт." in category.get_products

    def test_category_creation_empty(self):
        """Тест создания пустой категории."""
        category = Category("Пустая", "Категория")

        assert category.name == "Пустая"
        assert len(category) == 0
        assert category.get_products == ""

    def test_add_product(self):
        """Тест добавления товара в категорию."""
        category = Category("Категория", "Описание")
        product = Product("Товар", "Описание", 150.0, 3)

        category.add_product(product)
        assert len(category) == 1
        assert "Товар, 150.0 руб. Остаток: 3 шт." in category.get_products

    def test_add_invalid_product(self):
        """Тест добавления невалидного объекта в категорию."""
        category = Category("Категория", "Описание")

        with pytest.raises(TypeError):
            category.add_product("не продукт")

        with pytest.raises(TypeError):
            category.add_product(123)

    def test_counters(self):
        """Тест счетчиков категорий и товаров."""
        product1 = Product("Т1", "Оп1", 100.0, 1)
        product2 = Product("Т2", "Оп2", 200.0, 2)

        category1 = Category("Кат1", "Описание1", [product1])
        category2 = Category("Кат2", "Описание2", [product2])

        assert Category.category_count == 2
        assert Category.product_count == 0


    def test_counters_with_add_product(self):
        """Тест счетчиков при добавлении товаров после создания."""
        category = Category("Категория", "Описание")
        initial_count = Category.product_count

        product = Product("Товар", "Описание", 100.0, 1)
        category.add_product(product)

        assert Category.product_count == initial_count + 1

    def test_private_products_access(self):
        """Тест приватности атрибута продуктов."""
        category = Category("Категория", "Описание")
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_len_method(self):
        """Тест метода __len__."""
        category = Category("Категория", "Описание")
        assert len(category) == 0

        product = Product("Товар", "Описание", 100.0, 1)
        category.add_product(product)
        assert len(category) == 1

    def test_str_representation_empty(self):
        """Тест строкового представления пустой категории."""
        category = Category("Электроника", "Техника")
        expected = "Электроника, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_str_representation_with_products(self):
        """Тест строкового представления категории с товарами."""
        product1 = Product("Телефон", "Смартфон", 1000.0, 5)
        product2 = Product("Ноутбук", "Игровой", 2000.0, 3)
        category = Category("Электроника", "Техника", [product1, product2])

        expected = "Электроника, количество продуктов: 8 шт."  # 5 + 3
        assert str(category) == expected


def test_category_products_getter():
    """Тест геттера products в классе Category."""
    product1 = Product("Телефон", "Смартфон", 999.99, 10)
    product2 = Product("Ноутбук", "Игровой", 1500.0, 5)

    category = Category("Электроника", "Техника", [product1, product2])

    products_output = category.get_products

    # Проверяем точный формат вывода
    expected_line1 = "Телефон, 999.99 руб. Остаток: 10 шт."
    expected_line2 = "Ноутбук, 1500.0 руб. Остаток: 5 шт."

    assert expected_line1 in products_output
    assert expected_line2 in products_output


def test_category_products_getter_empty():
    """Тест геттера products для пустой категории."""
    category = Category("Пустая", "Категория")

    assert category.get_products == ""


def test_category_products_getter_single_product():
    """Тест геттера products для одного товара."""
    product = Product("Мышь", "Компьютерная", 25.5, 20)
    category = Category("Аксессуары", "Периферия", [product])

    expected = "Мышь, 25.5 руб. Остаток: 20 шт."
    assert category.get_products == expected


def test_product_addition_multiple():
    """Тест сложения нескольких продуктов."""
    product1 = Product("Товар1", "Описание1", 100.0, 2)  # 200
    product2 = Product("Товар2", "Описание2", 50.0, 4)  # 200
    product3 = Product("Товар3", "Описание3", 25.0, 8)  # 200

    # Складываем попарно, так как __add__ возвращает float
    total1 = product1 + product2  # 200 + 200 = 400
    total = total1 + (product3.price * product3.quantity)  # 400 + 200 = 600
    assert total == 600.0


class TestProductInheritance:
    """Тесты для наследования классов Product."""

    def test_smartphone_creation(self):
        """Тест создания смартфона."""
        smartphone = Smartphone(
            "iPhone 15", "Флагманский смартфон", 150000.0, 10,
            95.5, "15 Pro", 256, "Black"
        )

        assert smartphone.name == "iPhone 15"
        assert smartphone.price == 150000.0
        assert smartphone.quantity == 10
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"
        assert isinstance(smartphone, Product)

    def test_lawn_grass_creation(self):
        """Тест создания газонной травы."""
        grass = LawnGrass(
            "Газонная трава", "Элитная трава", 500.0, 20,
            "Россия", "7 дней", "Зеленый"
        )

        assert grass.name == "Газонная трава"
        assert grass.price == 500.0
        assert grass.quantity == 20
        assert grass.country == "Россия"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Зеленый"
        assert isinstance(grass, Product)

    def test_smartphone_str_representation(self):
        """Тест строкового представления смартфона."""
        smartphone = Smartphone(
            "Samsung", "Смартфон", 80000.0, 5,
            90.0, "S23", 128, "White"
        )

        expected = "Samsung, 80000.0 руб. Остаток: 5 шт."
        assert str(smartphone) == expected

    def test_lawn_grass_str_representation(self):
        """Тест строкового представления газонной травы."""
        grass = LawnGrass(
            "Трава", "Для газона", 300.0, 15,
            "США", "5 дней", "Темно-зеленый"
        )

        expected = "Трава, 300.0 руб. Остаток: 15 шт."
        assert str(grass) == expected


class TestProductAdditionInheritance:
    """Тесты сложения для наследованных классов."""

    def test_smartphone_addition_same_type(self):
        """Тест сложения смартфонов одного типа."""
        smartphone1 = Smartphone(
            "Phone1", "Описание1", 100000.0, 2,
            95.0, "Model1", 256, "Black"
        )  # 100000 * 2 = 200000

        smartphone2 = Smartphone(
            "Phone2", "Описание2", 80000.0, 3,
            92.0, "Model2", 128, "White"
        )  # 80000 * 3 = 240000

        total = smartphone1 + smartphone2
        assert total == 440000.0  # 200000 + 240000

    def test_lawn_grass_addition_same_type(self):
        """Тест сложения газонных трав одного типа."""
        grass1 = LawnGrass(
            "Grass1", "Описание1", 400.0, 5,
            "Россия", "7 дней", "Зеленый"
        )  # 400 * 5 = 2000

        grass2 = LawnGrass(
            "Grass2", "Описание2", 300.0, 4,
            "США", "5 дней", "Темный"
        )  # 300 * 4 = 1200

        total = grass1 + grass2
        assert total == 3200.0  # 2000 + 1200

    def test_smartphone_lawn_grass_addition_error(self):
        """Тест ошибки при сложении смартфона и газонной травы."""
        smartphone = Smartphone(
            "Phone", "Смартфон", 100000.0, 2,
            95.0, "Model", 256, "Black"
        )

        grass = LawnGrass(
            "Grass", "Трава", 400.0, 5,
            "Россия", "7 дней", "Зеленый"
        )

        with pytest.raises(TypeError, match="Можно складывать объекты только одного класса"):
            smartphone + grass

    def test_lawn_grass_smartphone_addition_error(self):
        """Тест ошибки при сложении газонной травы и смартфона."""
        grass = LawnGrass(
            "Grass", "Трава", 400.0, 5,
            "Россия", "7 дней", "Зеленый"
        )

        smartphone = Smartphone(
            "Phone", "Смартфон", 100000.0, 2,
            95.0, "Model", 256, "Black"
        )

        with pytest.raises(TypeError, match="Можно складывать объекты только одного класса"):
            grass + smartphone


class TestCategoryWithInheritedProducts:
    """Тесты категории с наследованными продуктами."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_add_smartphone_to_category(self):
        """Тест добавления смартфона в категорию."""
        category = Category("Смартфоны", "Мобильные устройства")
        smartphone = Smartphone(
            "iPhone", "Смартфон", 100000.0, 5,
            95.0, "15", 256, "Black"
        )

        category.add_product(smartphone)
        assert len(category) == 1
        assert "iPhone, 100000.0 руб. Остаток: 5 шт." in category.get_products

    def test_add_lawn_grass_to_category(self):
        """Тест добавления газонной травы в категорию."""
        category = Category("Сад", "Садовые товары")
        grass = LawnGrass(
            "Трава", "Газонная", 500.0, 10,
            "Россия", "7 дней", "Зеленый"
        )

        category.add_product(grass)
        assert len(category) == 1
        assert "Трава, 500.0 руб. Остаток: 10 шт." in category.get_products

    def test_add_mixed_products_to_category(self):
        """Тест добавления разных типов продуктов в категорию."""
        category = Category("Разное", "Разные товары")

        smartphone = Smartphone(
            "Phone", "Смартфон", 80000.0, 3,
            92.0, "Model", 128, "White"
        )

        grass = LawnGrass(
            "Grass", "Трава", 400.0, 8,
            "США", "5 дней", "Темный"
        )

        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category) == 2
        products_output = category.get_products
        assert "Phone, 80000.0 руб. Остаток: 3 шт." in products_output
        assert "Grass, 400.0 руб. Остаток: 8 шт." in products_output

    def test_category_str_with_inherited_products(self):
        """Тест строкового представления категории с наследованными продуктами."""
        smartphone = Smartphone(
            "Phone", "Смартфон", 100000.0, 2,
            95.0, "Model", 256, "Black"
        )

        grass = LawnGrass(
            "Grass", "Трава", 500.0, 3,
            "Россия", "7 дней", "Зеленый"
        )

        category = Category("Тест", "Категория", [smartphone, grass])

        expected = "Тест, количество продуктов: 5 шт."  # 2 + 3
        assert str(category) == expected


class TestProductProtection:
    """Тесты защиты от добавления не-продуктов в категорию."""

    def test_add_only_product_and_inherited(self):
        """Тест, что в категорию можно добавлять только Product и наследников."""
        category = Category("Защита", "Тест защиты")

        # Эти должны работать
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone("Phone", "Смартфон", 50000.0, 2, 90.0, "M", 128, "B")
        grass = LawnGrass("Grass", "Трава", 300.0, 4, "RU", "7д", "G")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category) == 3

    def test_add_invalid_types_errors(self):
        """Тест ошибок при добавлении невалидных типов."""
        category = Category("Защита", "Тест защиты")

        invalid_items = [
            "строка",
            123,
            45.67,
            ["список"],
            {"словарь": "значение"},
            None,
            True,
            (1, 2, 3)
        ]

        for invalid_item in invalid_items:
            with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
                category.add_product(invalid_item)

    def test_product_count_with_inherited(self):
        """Тест счетчика продуктов с наследованными классами."""
        Category.product_count = 0  # Сброс

        category = Category("Тест", "Категория")

        initial_count = Category.product_count

        product = Product("Товар", "Описание", 100.0, 1)
        smartphone = Smartphone("Phone", "Смартфон", 50000.0, 1, 90.0, "M", 128, "B")
        grass = LawnGrass("Grass", "Трава", 300.0, 1, "RU", "7д", "G")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert Category.product_count == initial_count + 3
