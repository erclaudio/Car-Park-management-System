
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone, timesince

from . registration_recognition import get_registration
from users.models import UserSession


User = get_user_model()


def parking():
    img_path = os.path.join(settings.BASE_DIR, 'carpark/vehicles/test4.jpeg')
    reg_number = get_registration(img_path)

    user = User.objects.filter(profile__reg=reg_number).first()
    if user is not None:
        if user.profile.parked == True:
            # finish parking logic
            elapsed_time = timesince.timesince(user.profile.parktime)
            time_delta = timezone.now() - user.profile.parktime
            total_minutes = time_delta.total_seconds() / 60
            amount = total_minutes * 0.05
            UserSession.objects.create(
                user=user, elapsed_time=elapsed_time, amount=amount)

            user.profile.parked = False
            user.profile.parktime = None
            user.save()

        else:
            # Make new park
            user.profile.parked = True
            user.profile.parktime = timezone.now()
            user.save()
    else:
        return False

    return True
