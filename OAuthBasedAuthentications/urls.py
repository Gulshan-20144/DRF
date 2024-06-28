from rest_framework.urls import path

from OAuthBasedAuthentications.views import OAuthView,OauthTokenApiView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"OAuthApiView",OAuthView,basename="OAuthApiView")
urlpatterns=[
    path("o/token/",OauthTokenApiView.as_view(),name="token")
]

urlpatterns +=router.urls