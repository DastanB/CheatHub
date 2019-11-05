from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token


from users.views import RegisterUserAPIView, UserViewSet

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', RegisterUserAPIView.as_view())
]


router = DefaultRouter()
router.register('users', UserViewSet, base_name='users')


urlpatterns += router.urls