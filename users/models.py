from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    # user_id = models.PositiveIntegerField('Id', unique=True)
    # username = models.CharField('Username', max_length=64, unique=True)
    # password = models.CharField('Password', max_length=64)
    # first_name = models.CharField('First name', max_length=64)
    # last_name = models.CharField('Last name', max_length=64)
    # date_joined = models.DateTimeField('Joined at', default=timezone.datetime.now())

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='User Profile')
    avatar_url = models.URLField('Avatar', max_length=160, null=False, db_index=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User's profile"
        verbose_name_plural = "User's profiles"

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.userprofile.save()
