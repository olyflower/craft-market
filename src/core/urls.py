from django.urls import path

from core.views import (EditUserProfileView, GetUserProfile, IndexView,
                        UserLogin, UserLogout, UserRegistration)

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("registration/", UserRegistration.as_view(), name="registration"),
    path("profile/", GetUserProfile.as_view(), name="profile"),
    path("edit-profile/<int:pk>/", EditUserProfileView.as_view(), name="edit_profile"),
]
