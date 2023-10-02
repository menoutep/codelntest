from django.contrib import admin
from base.models import Badge,Model3D,UserBadge
from accounts.models import MyCustomUser
# Register your models here.
admin.site.register(Badge)
admin.site.register(Model3D)
admin.site.register(UserBadge)
admin.site.register(MyCustomUser)