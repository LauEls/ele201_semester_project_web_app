from django.contrib import admin
from microcontroller_data.models import Chronometer
from microcontroller_data.models import SolarTracker
from microcontroller_data.models import Piano
from microcontroller_data.models import ImuLedArray
from microcontroller_data.models import RemoteControlledCar
from microcontroller_data.models import Smarthouse
from microcontroller_data.models import CandleLength

# Register your models here.
admin.site.register(Chronometer)
admin.site.register(SolarTracker)
admin.site.register(Piano)
admin.site.register(ImuLedArray)
admin.site.register(RemoteControlledCar)
admin.site.register(Smarthouse)
admin.site.register(CandleLength)