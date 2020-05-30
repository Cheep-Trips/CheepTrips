from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Region)
admin.site.register(Location)
admin.site.register(Activity)
admin.site.register(Flight)
admin.site.register(Trip)
admin.site.register(User)