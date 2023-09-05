from rest_framework import serializers
from .models import Category, Book, Customer, Order, Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'category']


class CreateBookSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        if Category.objects.filter(pk=category_id).exists():
            return category_id
        raise serializers.ValidationError({'error': 'Category id not valid !'})

    class Meta:
        model = Book
        fields = ['id', 'name', 'category_id']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address', 'college', 'user']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'book', 'quantity', 'placed_at']


class CreateOrderSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, book_id):
        if Book.objects.filter(pk=book_id).exists():
            return book_id
        raise serializers.ValidationError({'error': 'Book id invalid !'})

    def save(self, **kwargs):
        book_id = self.validated_data['book_id']
        user_id = self.context.get('user_id')
        book = Book.objects.get(pk=book_id)
        customer = Customer.objects.get(user_id=user_id)

        try:

            order = Order.objects.get(customer=customer, book=book)
            # update quantity
            order.quantity += 1
            order.save()
        except Order.DoesNotExist:
            # create new order
            Order.objects.create(
                customer=customer, book=book, quantity=1)
        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['quantity']
