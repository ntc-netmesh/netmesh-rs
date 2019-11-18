from django.contrib import admin
from netmesh_api import models


admin.site.register(models.Test)
admin.site.register(models.DataPoint)
admin.site.register(models.Server)
admin.site.register(models.AgentProfile)
admin.site.register(models.UserProfile)
admin.site.register(models.RFC6349TestDevice)

