from django.db import models
from admin_panel.models import CustomUser

class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OTP for {self.user.username}'

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='First')
    last_name = models.CharField(max_length=100, default='Last')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    housename = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.first_name},{self.housename}, {self.street}, {self.city}, {self.state} - {self.zipcode}'


