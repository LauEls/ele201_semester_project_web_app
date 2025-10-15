from django.shortcuts import render
from rest_framework import generics, viewsets
from microcontroller_data.models import Chronometer, SolarTracker, Piano, ImuLedArray, RemoteControlledCar, Smarthouse, CandleLength
from microcontroller_data.serializers import ChronometerSerializer, SolarTrackerSerializer, PianoSerializer, ImuLedArraySerializer, RemoteControlledCarSerializer, SmarthouseSerializer, CandleLengthSerializer

# Create your views here.
class ChronometerViewSet(viewsets.ModelViewSet):
    queryset = Chronometer.objects.all()
    serializer_class = ChronometerSerializer

class SolarTrackerViewSet(viewsets.ModelViewSet):
    queryset = SolarTracker.objects.all()
    serializer_class = SolarTrackerSerializer

class PianoViewSet(viewsets.ModelViewSet):
    queryset = Piano.objects.all()
    serializer_class = PianoSerializer

class ImuLedArrayViewSet(viewsets.ModelViewSet):
    queryset = ImuLedArray.objects.all()
    serializer_class = ImuLedArraySerializer

class RemoteControlledCarViewSet(viewsets.ModelViewSet):
    queryset = RemoteControlledCar.objects.all()
    serializer_class = RemoteControlledCarSerializer

class SmarthouseViewSet(viewsets.ModelViewSet):
    queryset = Smarthouse.objects.all()
    serializer_class = SmarthouseSerializer

class CandleLengthViewSet(viewsets.ModelViewSet):
    queryset = CandleLength.objects.all()
    serializer_class = CandleLengthSerializer
