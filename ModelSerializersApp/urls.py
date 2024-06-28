from rest_framework.urls import path

from ModelSerializersApp.views import ModelSerializersView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"ModelSerializersApp_app",ModelSerializersView,basename="ModelSerializersApp_app")
urlpatterns=[

]

urlpatterns +=router.urls