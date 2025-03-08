from django.urls import path

from . import views

app_name = 'elements'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:pk>', views.detail, name='detail'),
    path('<str:slug>', views.detail, name='detail'),
    path('capture-payment/<str:order_id>', views.capture_payment, name='capture_payment'),
]