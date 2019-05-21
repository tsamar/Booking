from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, MasterProfile, ServiceType, Schedule, Booking


admin.site.register(User)
admin.site.register(MasterProfile)
admin.site.register(ServiceType)
admin.site.register(Schedule)
admin.site.register(Booking)


