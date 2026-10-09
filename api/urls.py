from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('myproducts/', views.my_product_lists),
    path('myproducts/<int:id>', views.my_product_list),
    path('myorders/', views.my_order_list),
    path('myordersitem/', views.my_orderitem_list),
    # path('myproductcreate/', views.MyProductCreateAPIView.as_view()),
    path('myproductlistcreate/', views.MyProductListCreateAPIView.as_view()),

    ##################################################################
    path('products/', views.ProductListCreateAPIView.as_view()),
    # path('products/create', views.ProductCreateAPIView.as_view()),
    path('products/<int:product_id>', views.ProductDetailAPIView.as_view()),
    path('productinfo/', views.product_info),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls