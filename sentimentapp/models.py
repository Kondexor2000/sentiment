from django.db import models

# Create your models here.

# w pliku models.py w aplikacji
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Lekarz(CustomUser):
    # Tu możesz dodać specyficzne dla lekarza pola, jeśli są potrzebne
    # Na przykład:
    specyficzne_dla_lekarza_pole = models.CharField(max_length=100)

class Inzynier(CustomUser):
    # Tu możesz dodać specyficzne dla inżyniera pola, jeśli są potrzebne
    # Na przykład:
    specyficzne_dla_inzyniera_pole = models.CharField(max_length=100)

class Slowo(models.Model):
    slowo = models.CharField(max_length=50, unique=True)
    jest_pozytywne = models.BooleanField(default=False)

    def __str__(self):
        return self.slowo

class Opinia(models.Model):
    tresc = models.TextField()
    punkty = models.IntegerField(default=0)
    lekarz = models.ForeignKey(Lekarz, on_delete=models.CASCADE, related_name='opinie_lekarza', null=True, blank=True)
    inzynier = models.ForeignKey(Inzynier, on_delete=models.CASCADE, related_name='opinie_inzyniera', null=True, blank=True)

    def __str__(self):
        return self.tresc

class Sentyment(models.Model):
    inzynier = models.OneToOneField(Inzynier, on_delete=models.CASCADE, related_name='sentyment', null=True, blank=True)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"Sentyment dla {self.inzynier}"
