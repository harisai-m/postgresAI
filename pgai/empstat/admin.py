from django.contrib import admin
from .models import Employee,Fuelconsumption,WeatherData,Sales

# Register your models here.
admin.site.register(Employee)
admin.site.register(Fuelconsumption)
admin.site.register(WeatherData)
admin.site.register(Sales)
