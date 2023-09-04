from rest_framework import serializers
from .models import Category, Book, Customer, Order


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
