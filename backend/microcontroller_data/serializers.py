from rest_framework import serializers
from microcontroller_data.models import Chronometer, SolarTracker, Piano, ImuLedArray, RemoteControlledCar, Smarthouse, CandleLength, RegisteredDevices

class ChronometerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chronometer
        fields = ('mac_address', 'state', 'elapsed_time', 'timestamp')

class SolarTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarTracker
        fields = ('__all__')

class PianoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piano
        fields = ('__all__')

class ImuLedArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImuLedArray
        fields = ('__all__')

class RemoteControlledCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteControlledCar
        fields = ('__all__')

class SmarthouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smarthouse
        fields = ('__all__')

class CandleLengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandleLength
        fields = ('__all__')

class RegisteredDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredDevices
        fields = ('__all__')