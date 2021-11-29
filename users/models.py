from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from users.choices import user_type, status, gender


def get_image_filename(instance, filename):
    return 'users/%s/'%(filename)
    

class EcomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,**extra_fields)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, first_name, last_name, password,  **extra_fields)


class EcomUser(AbstractBaseUser, PermissionsMixin):
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)    
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(choices=user_type,max_length=10,default='CUS')
    mobile_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    images = models.ImageField(default='default.png',blank=True, null=True,upload_to=get_image_filename)
    about = models.CharField(max_length=500, unique=True, null=True, blank=True)
    status = models.CharField(choices=status,max_length=10, default='AV')
    gender = models.CharField(choices=gender,max_length=5,null=True,blank=True)
    d_o_b =  models.DateField(null=True, blank=True)
    tenant_admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = EcomUserManager()

    def __str__(self):
        return self.email