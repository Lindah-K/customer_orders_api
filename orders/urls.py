from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet
from mozilla_django_oidc.views import OIDCAuthenticationRequestView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('oidc/login/', OIDCAuthenticationRequestView.as_view(), name='oidc_login'),
]



