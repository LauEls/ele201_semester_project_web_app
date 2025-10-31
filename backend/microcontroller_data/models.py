from django.db import models

# Create your models here.
class Chronometer(models.Model):
    mac_address = models.CharField(max_length=17)
    state = models.PositiveIntegerField()
    elapsed_time = models.FloatField()
    timestamp = models.FloatField()

class SolarTracker(models.Model):
    mac_address = models.CharField(max_length=17)
    servo_angle = models.FloatField()
    light_intensity = models.FloatField()
    timestamp = models.FloatField()

class Piano(models.Model):
    mac_address = models.CharField(max_length=17)
    note = models.CharField(max_length=7)
    timestamp = models.FloatField()

class ImuLedArray(models.Model):
    mac_address = models.CharField(max_length=17)
    imu_angle = models.FloatField()
    timestamp = models.FloatField()

class RemoteControlledCar(models.Model):
    mac_address = models.CharField(max_length=17)
    velocity = models.FloatField()
    linear_input = models.FloatField()
    angular_input = models.FloatField()
    timestamp = models.FloatField()

class Smarthouse(models.Model):
    mac_address = models.CharField(max_length=17)
    temperature = models.CharField()
    motion_detected = models.BooleanField()
    timestamp = models.FloatField()

class CandleLength(models.Model):
    mac_address = models.CharField(max_length=17)
    candle_length = models.FloatField()
    elapsed_time = models.FloatField()
    timestamp = models.FloatField()

class RegisteredDevices(models.Model):
    mac_address = models.CharField(max_length=17)
    device_name = models.CharField(max_length=32)