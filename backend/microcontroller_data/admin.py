from django.contrib import admin
from microcontroller_data.models import Chronometer, SolarTracker, Piano, ImuLedArray, RemoteControlledCar, Smarthouse, CandleLength, RegisteredDevices


# Register your models here.
admin.site.register(Chronometer)
admin.site.register(SolarTracker)
admin.site.register(Piano)
admin.site.register(ImuLedArray)
admin.site.register(RemoteControlledCar)
admin.site.register(Smarthouse)
admin.site.register(CandleLength)
admin.site.register(RegisteredDevices)