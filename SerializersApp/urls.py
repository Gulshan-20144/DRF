from rest_framework.urls import path
from SerializersApp.views import *
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"api/Serializers_app",BuyBooksView,basename="Serializers_app")
urlpatterns=[

]

urlpatterns +=router.urls