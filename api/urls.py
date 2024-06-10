from django.urls import path
from . import views

urlpatterns = [
    path('', views.serverStatus.as_view()),
    path('public/', views.public),
    path('share/', views.redirect_to_product_link)
]