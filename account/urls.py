from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from account import views

router = SimpleRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]
