from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('public/', views.public),
    path('api/share/', views.redirect_to_product_link)
]