from rest_framework.urls import path
from SerializersApp.views import *
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"BaseSerializers_app",BuyBooksView,basename="BaseSerializers_app")
urlpatterns=[

]

urlpatterns +=router.urls