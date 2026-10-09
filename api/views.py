from django.shortcuts import render, get_object_or_404
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, MyOrderSerializer, MyOrderItemSerializer
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import Product, Order, OrderItem
from rest_framework.response import Response    
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .filters import ProductFilter, OrderFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
    
# Create your views here.

# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.exclude(stock__gt = 0)
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'price', 'stock']
    search_fields = ['name', 'description']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param = 'size' #allow clients to choose the number of records per page.

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [ IsAdminUser ]
        return super().get_permissions()


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            self.permission_classes = [ IsAdminUser ]
        return super().get_permissions()

# @api_view(['GET'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk = id)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer


# @api_view(['GET'])
# def order_list(request):
#     order = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(order, many=True)
#     return Response(serializer.data)


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user = request.user)
        return qs


    # @action(detail=False, methods=['get'], url_path='user-orders',permission_classes=[IsAuthenticated])
    # @action(detail=False, methods=['get'], url_path='user-orders')
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user = request.user)
    #     serialzer = self.get_serializer(orders, many=True)
    #     return Response(serialzer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)




#Function based views
# def my_product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return JsonResponse({'data': serializer.data})

@api_view(['GET', 'POST'])
def my_product_lists(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        parsed_data = request.data
        serializer = ProductSerializer(data = parsed_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'creation':'successfull'})

@api_view(['GET', 'POST'])
def my_product_list(request, id):
    if request.method == "GET":
        product = get_object_or_404(Product, id = id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

@api_view(['GET'])
def my_order_list(request):
    orders = Order.objects.all()
    serializer = MyOrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def my_orderitem_list(request):
    orders = OrderItem.objects.all()
    serializer = MyOrderItemSerializer(orders, many=True)
    return Response(serializer.data)


class MyOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)

class MyProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer


class MyProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ('name', 'price')

    def get_permissions(self, request):
        self.permission_classes = [AllowAny]
        if request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()