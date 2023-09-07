from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter
from .permissons import IsAdminOrReadOnly
from .serializers import CategorySerializer, BookSerializer, CreateBookSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .models import Book, Category, Customer, Order
from .filters import CustomFilter


# Create your views here.


class CategoryViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'put', 'delete']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        # book associate with category that's why we override this function
        if Book.objects.filter(category_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'category delete not possible it associate with book !'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomFilter
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        # book associate with order
        if Order.objects.filter(book_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Book Delete not possible it associate with order !'})
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CreateBookSerializer
        return BookSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [AllowAny()]

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


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    queryset = Order.objects.select_related(
        'customer').all().select_related('book')
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={
                                           'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_queryset(self):
        customer = Customer.objects.get(user_id=self.request.user.id)
        return Order.objects.filter(customer=customer)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}
