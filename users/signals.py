from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.BASE_URL}/users/activate/{instance.id}/{token}/"
        send_mail(
            "Activate your account",
            f"Click here to activate your account: {activation_url}",
            settings.EMAIL_HOST_USER,
            [instance.email]
        )
