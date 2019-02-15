from django.contrib import admin

# Register your models here.
from testgale.core.models import Crawler, Link, Image

admin.site.register(Crawler)
admin.site.register(Link)
admin.site.register(Image)

