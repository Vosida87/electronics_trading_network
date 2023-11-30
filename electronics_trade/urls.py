from electronics_trade.apps import ElectronicsTradeConfig
from rest_framework import routers
from electronics_trade.views import ParticipantViewSet
from django.urls import include, path

app_name = ElectronicsTradeConfig.name

router = routers.DefaultRouter()
router.register('participants', ParticipantViewSet)

urlpatterns = [
    path('/', include(router.urls)),
]
