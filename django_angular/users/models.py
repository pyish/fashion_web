from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobi_number = models.IntegerField()
    delivery_address = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name_plural = 'Addresses'


class MpesaCode(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code