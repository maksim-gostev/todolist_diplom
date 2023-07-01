from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='регистрация'),
    path('login', views.UserLoginView.as_view(), name='авторизация'),
    path('profile', views.ProfileView.as_view(), name='профиль'),
    path('update_password', views.ChangingPasswordView.as_view(), name='изменение пороля'),
]
