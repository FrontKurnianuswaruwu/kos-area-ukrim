from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    idNama = models.CharField(max_length=10,primary_key=True)
    user_name = models.CharField(max_length=30)
    NoTelp = models.CharField(max_length=12)
    email = models.EmailField(max_length=254, default=None)
    password = models.CharField(max_length=50, default=None)
    
    
class KamarKost(models.Model):
    idKamar= models.CharField(max_length=100 )
    TIPEKAMAR_CHOICES = [
        ('premium', 'Premium'),
        ('standard', 'Standard'),
    ]
    TipeKamar = models.CharField(max_length=10, choices=TIPEKAMAR_CHOICES, null=True)
    Harga = models.CharField(max_length=50)
    FasilitasKOst= models.CharField(max_length=250)
    masaTenggang = models.CharField(max_length=10)
    gambar = models.ImageField(upload_to='static/img/kamar',null=True)
    namakost = models.CharField(null=True,max_length=50)
    alamat = models.URLField(default='https://maps.google.com')
    kodeadmin = models.ForeignKey(Admin, on_delete=models.CASCADE, null='True')
    STATUS_CHOICES = [
        ('available', 'Tersedia'),
        ('occupied', 'Terisi'),
        ('under_repair', 'Dalam Perbaikan'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, null=True)
    GENDER_CHOICES = [
        ('putra', 'Putra'),
        ('putri', 'Putri'),
    ]
    status_kamar = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)

class penghuni(models.Model):
    IdKamar= models.CharField(max_length=100)
    NoTelepon = models.CharField(max_length=12)
    ktp = models.CharField(max_length=16)
    kodeadminpenghuni = models.ForeignKey(Admin, on_delete=models.CASCADE, null='True')
    
    
 

