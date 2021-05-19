from django.db import models
from data_models.models import BaseModel, BaseUserModel
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User", editable=False)
    mobile = PhoneField(blank=True, null=True, verbose_name="Mobile")
    avatar = models.ImageField(blank=True, null=True, verbose_name="Avatar")

    def __str__(self):
        return self.user.username


class ActivityItems(models.IntegerChoices):
    DEFAULT = (0, "Default")
    CONNECT = (1, "Connect")
    DISCONNECT = (2, "Disconnect")


class History(BaseUserModel):
    activity = models.IntegerField(choices=ActivityItems.choices, default=ActivityItems.DEFAULT, blank=False)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return "{}: {} - {}".format(self.user.username, self.get_activity_display(), self.created_at)


@receiver(post_save, sender=User)
def new_profile(sender, instance, created, **kwargs):
    if created and instance:
        Profile.objects.create(user=instance)
