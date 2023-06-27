from django.urls import path

from core import views

urlpatterns = [path('signup', views.SignUpView.as_view()), path('login', views.UserLoginView.as_view())]
