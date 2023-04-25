from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from account.models import UserProfile
from core.forms import UserProfileForm, UserRegistrationForm


class IndexView(TemplateView):
    template_name = "../templates/index.html"
    http_method_names = ["get"]
    extra_context = {"site_name": "Craft-Market"}


class UserLogin(LoginView):
    ...


class UserLogout(LogoutView):
    ...


class UserRegistration(CreateView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        _form = super().form_valid(form)
        login(self.request, self.object)
        return _form


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
