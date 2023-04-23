from django.urls import path

from core.views import IndexView, UserLogin, UserLogout, UserRegistration

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("registration/", UserRegistration.as_view(), name="registration"),
]
