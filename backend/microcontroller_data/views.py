from django.shortcuts import render
from rest_framework import generics, viewsets
from microcontroller_data.models import Chronometer, SolarTracker, Piano, ImuLedArray, RemoteControlledCar, Smarthouse, CandleLength, RegisteredDevices
from microcontroller_data.serializers import ChronometerSerializer, SolarTrackerSerializer, PianoSerializer, ImuLedArraySerializer, RemoteControlledCarSerializer, SmarthouseSerializer, CandleLengthSerializer, RegisteredDevicesSerializer
from django_eventstream.viewsets import EventsViewSet
from django_eventstream import send_event

# Create your views here.
class ChronometerViewSet(viewsets.ModelViewSet):
    queryset = Chronometer.objects.all()
    serializer_class = ChronometerSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('chronometer-channel', 'chronometer-msg', data)

class SolarTrackerViewSet(viewsets.ModelViewSet):
    queryset = SolarTracker.objects.all()
    serializer_class = SolarTrackerSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('solar-tracker-channel', 'solar-tracker-msg', data)

class PianoViewSet(viewsets.ModelViewSet):
    queryset = Piano.objects.all()
    serializer_class = PianoSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('piano-channel', 'piano-msg', data)

class ImuLedArrayViewSet(viewsets.ModelViewSet):
    queryset = ImuLedArray.objects.all()
    serializer_class = ImuLedArraySerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('imu-channel', 'imu-msg', data)

class RemoteControlledCarViewSet(viewsets.ModelViewSet):
    queryset = RemoteControlledCar.objects.all()
    serializer_class = RemoteControlledCarSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('car-channel', 'car-msg', data)

class SmarthouseViewSet(viewsets.ModelViewSet):
    queryset = Smarthouse.objects.all()
    serializer_class = SmarthouseSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('smarthouse-channel', 'smarthouse-msg', data)

class CandleLengthViewSet(viewsets.ModelViewSet):
    queryset = CandleLength.objects.all()
    serializer_class = CandleLengthSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        data = self.get_serializer(instance).data
        send_event('candle-channel', 'candle-msg', data)

class RegisteredDevicesViewSet(viewsets.ModelViewSet):
    queryset = RegisteredDevices.objects.all()
    serializer_class = RegisteredDevicesSerializer
