from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("profile/<int:pk>",views.user_view,name="profile"),
    path("create",views.create,name="create"),
    path("poem/<int:pk>",views.poem_view,name="poem_view"),





]
