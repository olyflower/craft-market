from django import forms

from account.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["gender", "address", "payment_method", "social_media_profiles"]
