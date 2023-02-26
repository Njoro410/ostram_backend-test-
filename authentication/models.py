from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):

        if not email:
            raise ValueError("Email is required")

        if not username:
            raise ValueError("Username is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return
 