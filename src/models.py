from abc import ABC, abstractmethod


class BaseProduct(ABC):


    @classmethod
    @abstractmethod
    def new_product(cls, product_data):
        pass


    @property
    @abstractmethod
    def price(self):
        pass


    @abstractmethod
    def __str__(self):
        pass


class ReprMixin:
    """
    Упрощенный миксин - логирует только факт создания
    """

    def __init__(self, *args, **kwargs):
        print(f"Создан объект: {self.__class__.__name__}")
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}()"  # Простой вывод

class Product(ReprMixin, BaseProduct):
    """Класс для представления товара."""

    def __init__(self, name, description, price, quantity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        if self.quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")


    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if isinstance(other, Product):
            if type(other) == type(self):
                return (self.price * self.quantity) + (other.price * other.quantity)
            raise TypeError("Можно складывать объекты только одного класса")
        raise TypeError("Можно складывать только объекты Product")

    @classmethod
    def new_product(cls, product_data):
        required_fields = ['name', 'description', 'price', 'quantity']
        for field in required_fields:
            if field not in product_data:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1


    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


    def add_product(self, product):
        # Вместо сложной проверки используйте просто isinstance
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(product)
        Category.product_count += 1


    @property
    def get_products(self):
        """Геттер для вывода списка товаров в требуемом формате."""
        products_list = []
        for product in self.__products:
            products_list.append(str(product))
        return "\n".join(products_list)


    def __len__(self):
        return len(self.__products)


    def middle_price(self):
        try:
            summ = 0
            for product in self.__products:
                summ +=product.price
            return summ / len(self.__products)
        except:
            return 0


class Smartphone(Product):
    def __init__(self,  name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
