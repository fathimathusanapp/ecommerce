#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from django.conf import settings
#from account.models import  Address
#from admin_panel.models import CustomUser

#@receiver(post_save, sender=CustomUser)
#def save_user_address(sender, instance, created, **kwargs):
    # Create a Profile when a new CustomUser is created
  #  if created:
   #     Address.objects.create(user=instance)
    #else:
   #     instance.Address.save()

    # Check if an Address for the user exists, create it if not
  #  if not Address.objects.filter(user=instance).exists():
   #     Address.objects.create(user=instance)
