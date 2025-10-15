from django.urls import path
from microcontroller_data.views import ChronometerViewSet, SolarTrackerViewSet, PianoViewSet, ImuLedArrayViewSet, RemoteControlledCarViewSet, SmarthouseViewSet, CandleLengthViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chronometer', ChronometerViewSet)
router.register('solar-tracker', SolarTrackerViewSet)
router.register('piano', PianoViewSet)
router.register('imu-led-array', ImuLedArrayViewSet)
router.register('remote-controlled-car', RemoteControlledCarViewSet)
router.register('smarthouse', SmarthouseViewSet)
router.register('candle-length', CandleLengthViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path('microcontroller_data/', ChronometerListAPIView.as_view()),
# ]