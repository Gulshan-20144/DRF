from rest_framework.urls import path

from JwtAuthenticationApp.views import JwtAuthenticationsViewsetView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"JwtAuthenticationsViewsetViews",JwtAuthenticationsViewsetView,basename="JwtAuthenticationsViewsetViews")
urlpatterns=[

]

urlpatterns +=router.urls