from __future__ import unicode_literals

from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'uploads.core'
    def ready(self):
        print("ready")