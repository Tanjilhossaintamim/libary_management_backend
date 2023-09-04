from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissons import IsAdminOrReadOnly
from .serializers import CategorySerializer, BookSerializer, CreateBookSerializer, CustomerSerializer
from .models import Book, Category, Customer, Order


# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Book.objects.filter(category_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'category delete not possible it associate with book !'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        if Order.objects.filter(book_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Book Delete not possible it associate with order !'})
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateBookSerializer
        return BookSerializer


class CustomerViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
