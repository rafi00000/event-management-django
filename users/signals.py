from django.shortcuts import redirect
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from event.models import Event

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONT_END_URL}users/activate/{instance.id}/{token}/"
        send_mail(
            "Activate your account",
            f"Click here to activate your account: \n {activation_url}",
            settings.EMAIL_HOST_USER,
            [instance.email]
        )
        redirect("home-page")

@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.participants.get(pk=user_id) 
            send_mail(
                "RSVP Confirmation",
                f"Thank you for RSVPing to {instance.name}. The event will be held on {instance.date} at {instance.location}.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False, 
            )

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        participant_group, _ = Group.objects.get_or_create(name="Participant")
        instance.groups.add(participant_group)
        instance.save()

