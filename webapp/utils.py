import os

import django
from django.conf import settings

from webapp import webapp

settings.configure(default_settings=webapp, DEBUG=True)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

django.setup()

from webapp.profile_user.models import Profile


def get_profiles():
    return Profile.objects.all()
