from django.urls import path, include
from microcontroller_data.views import ChronometerViewSet, SolarTrackerViewSet, PianoViewSet, ImuLedArrayViewSet, RemoteControlledCarViewSet, SmarthouseViewSet, CandleLengthViewSet, RegisteredDevicesViewSet
from rest_framework.routers import DefaultRouter
from django_eventstream.viewsets import EventsViewSet, configure_events_view_set

router = DefaultRouter()
router.register('chronometer', ChronometerViewSet)
router.register(
    "events",
    configure_events_view_set(channels=["chronometer-channel", "solar-tracker-channel", "piano-channel", "imu-channel", "car-channel", "smarthouse-channel", "candle-channel"],
    messages_types=["chronometer-msg", "solar-tracker-msg", "piano-msg", "imu-msg", "car-msg", "smarthouse-msg", "candle-msg"]),
    basename="events")
router.register('solar-tracker', SolarTrackerViewSet)
router.register('piano', PianoViewSet)
router.register('imu-led-array', ImuLedArrayViewSet)
router.register('remote-controlled-car', RemoteControlledCarViewSet)
router.register('smarthouse', SmarthouseViewSet)
router.register('candle-length', CandleLengthViewSet)
router.register('registered-devices', RegisteredDevicesViewSet)
# urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
]
# urlpatterns = [
#     path('microcontroller_data/', ChronometerListAPIView.as_view()),
# ]