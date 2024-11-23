from django.db import models

class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Temporarily store OTP if needed

    def __str__(self):
        return self.email
