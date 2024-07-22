from django.urls import path

from . import views


urlpatterns = [    
    path('',views.home,name='home'),
    path('About_Us/',views.About_Us,name='About_Us'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('product/',views.product,name='product'),
    path('edit_users/<int:id>/',views.edit_users,name='edit_users'),
    path('category/<str:category>/',views.products_by_category,name='products_by_category'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
    path('removecart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('size_chart',views.size_chart_form,name='size_chart_form'),
]