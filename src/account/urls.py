from django.urls import path

from account.views import EditUserProfileView, GetUserProfile

app_name = "account"

urlpatterns = [
    path("profile/", GetUserProfile.as_view(), name="profile"),
    path("edit-profile/<int:pk>/", EditUserProfileView.as_view(), name="edit_profile"),
]
