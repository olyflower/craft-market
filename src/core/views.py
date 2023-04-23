from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.forms import UserRegistrationForm


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
    success_url = reverse_lazy("core:success_registration")

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.is_active = False
    #     self.object.save()
    #
    #     send_registration_email(request=self.request, user_instance=self.object)
    #
    #     return super().form_valid(form)
