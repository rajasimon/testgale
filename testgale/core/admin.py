from django.contrib import admin

# Register your models here.
from testgale.core.models import Crawler, Image

admin.site.register(Crawler)
admin.site.register(Image)

