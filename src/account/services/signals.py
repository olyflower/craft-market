from account.models import UserProfile


def create_user_profile_signal(sender, instance, created: bool, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
