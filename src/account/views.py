from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from account.forms import UserProfileForm
from account.models import UserProfile


class GetUserProfile(TemplateView):
    template_name = "registration/profile.html"


class EditUserProfileView(UpdateView):
    login_url = "core:login"
    model = UserProfile
    form_class = UserProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("core:profile")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
