from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("profile/<int:pk>",views.user_view,name="profile"),
    path("create_1",views.create_1,name="create_1"),




]
