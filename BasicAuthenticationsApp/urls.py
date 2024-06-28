from rest_framework.urls import path

from BasicAuthenticationsApp.views import AuthenticationsViewsetView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"AuthenticationsViewsetViews",AuthenticationsViewsetView,basename="AuthenticationsViewsetViews")
urlpatterns=[

]

urlpatterns +=router.urls