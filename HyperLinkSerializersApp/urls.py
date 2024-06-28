from rest_framework.urls import path
from HyperLinkSerializersApp.views import *
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"HyperlinkSerializers_app",HyperSerializerView,basename="bookstore")
urlpatterns=[
    
]

urlpatterns +=router.urls
