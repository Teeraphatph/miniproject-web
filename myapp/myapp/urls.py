from django.contrib import admin
from django.urls import path
from .views import index,register_view,product, product_admin, add_product, update_product, delete_product, product_detail,updateItem,admin_order,checkout,payment_success,process_payment,update_profile,change_password 
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('product/', views.product,name='product'),
    path('product_admin', views.product_admin,name='product_admin'),
    path('product/add', views.add_product, name='add_product'),
    path('product/update/<int:product_id>', views.update_product, name='update_product'),
    path('product/delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('food3', views.food3),
    path('profile', views.profile),
    path('list_user', views.list_user,name='list_user'),
    path('login',views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('backend', views.backend_view, name='backend'),
    path('logout', views.logout),
    path('product/<int:product_id>', product_detail, name='product_detail'),
    path('product/<int:product_id>/upload_image/', views.upload_product_image, name='upload_product_image'),
    path('update_item', views.updateItem, name='update_item'),
    path('cart', views.cart, name='cart'),
    path('admin_order', views.admin_order, name='admin_order'),
    path('search/', views.search_product, name='search_product'),
    path('checkout/', checkout, name='checkout'),
    path('process_payment/', process_payment, name='process_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('update_profile/', update_profile, name='update_profile'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('change_password/', views.change_password, name='change_password'),
    path('search/update_item', views.updateItem, name='update_item'),
    path('product/update_item', views.updateItem, name='update_item'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
