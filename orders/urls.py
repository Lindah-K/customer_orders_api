from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet
from mozilla_django_oidc.views import OIDCAuthenticationResponseView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', OIDCAuthenticationResponseView.as_view(), name='oidc_login')
]


