from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import MSMEProfile, BuyerProfile, LenderProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.user_type == 'MSME':
                MSMEProfile.objects.get_or_create(user=instance)
            elif instance.user_type == 'BUYER':
                BuyerProfile.objects.get_or_create(user=instance)
            elif instance.user_type == 'LENDER':
                LenderProfile.objects.get_or_create(user=instance)
        except Exception as e:
            print(f"Error creating profile: {e}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.user_type == 'MSME' and hasattr(instance, 'msmeprofile'):
            instance.msmeprofile.save()
        elif instance.user_type == 'BUYER' and hasattr(instance, 'buyerprofile'):
            instance.buyerprofile.save()
        elif instance.user_type == 'LENDER' and hasattr(instance, 'lenderprofile'):
            instance.lenderprofile.save()
    except Exception as e:
        print(f"Error saving profile: {e}")