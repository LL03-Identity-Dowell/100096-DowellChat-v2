from django.contrib import admin
from django.urls import path, include
from api.views import SSLVerificationView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('.well-known/pki-validation/5F16A99CAF05B4C78E2CC29717284173.txt', SSLVerificationView.as_view(), name='ssl_verification'),
]
