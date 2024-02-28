from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
        return self.is_admin

class Closet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255, null=True, blank=True)                             
    cloth_type = models.CharField(max_length=100)                         # string으로 front에서 처리

class Level(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manner_level = models.IntegerField(default=0, null = False, blank = False)
    water_level = models.IntegerField(default=0, null = False, blank = False)
    tree_level = models.IntegerField(default=0, null = False, blank = False)