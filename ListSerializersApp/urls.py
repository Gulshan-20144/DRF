from rest_framework.urls import path

from ListSerializersApp.views import ListSerializersApiView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"^",ListSerializersApiView,basename="ModelSerializersApp_app")
urlpatterns=[

]

urlpatterns +=router.urls