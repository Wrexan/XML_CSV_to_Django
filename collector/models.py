from django.db import models


class User(models.Model):
    # user_id = models.PositiveIntegerField('Id', unique=True)
    username = models.CharField('Username', max_length=64, unique=True)
    password = models.CharField('Password', max_length=64)
    first_name = models.CharField('First name', max_length=64)
    last_name = models.CharField('Last name', max_length=64)
    date_joined = models.DateTimeField('Joined at')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='User')
    avatar_url = models.SlugField('Avatar', max_length=160)

    class Meta:
        verbose_name = "User's profile"
        verbose_name_plural = "User's profiles"
