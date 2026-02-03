from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def assign_member_group(sender, instance, created, **kwargs):
    if not created:
        return

    member_group = Group.objects.filter(name="Member").first()
    if member_group:
        instance.groups.add(member_group)
