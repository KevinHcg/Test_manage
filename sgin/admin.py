from django.contrib import admin
from sgin import models
# Register your models here.
admin.site.register(models.Event)
admin.site.register(models.Guest)
admin.site.register(models.Demand)
admin.site.register(models.DemandEvent)
admin.site.register(models.City)
admin.site.register(models.Report)
admin.site.register(models.Version)
admin.site.register(models.VersionEvent)