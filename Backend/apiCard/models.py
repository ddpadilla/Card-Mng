from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
import uuid

# Create your models here.


class User(models.Model):
    id_user = models.CharField(primary_key=True, max_length=13, validators=[MinLengthValidator(13)])
    full_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = self.full_name.lower().replace(' ', '-')
            self.slug = f"{base_slug}-{self.id_user}"
        super().save(*args, **kwargs)


class ParkingCard(models.Model):
    STATE_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]
    card_number = models.CharField(primary_key=True, max_length=8, validators=[MinLengthValidator(6)])
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='active')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"card-{self.card_number}"
        super().save(*args, **kwargs)

    
class Vehicle(models.Model):
    car_plate = models.CharField(max_length=8, primary_key=True, validators=[MinLengthValidator(6)])
    card_number = models.ForeignKey(ParkingCard, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Document(models.Model):
    id_document = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    card_number = models.ForeignKey(ParkingCard, on_delete=models.CASCADE)
    authorization_document = models.FileField(
        upload_to='documentos/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)