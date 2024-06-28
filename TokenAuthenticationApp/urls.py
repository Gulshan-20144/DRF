from rest_framework.urls import path

from TokenAuthenticationApp.views import CustomObtainAuthToken, TokenAuthenticationsViewsetView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"TokenAuthenticationsViewsetView",TokenAuthenticationsViewsetView,basename="TokenAuthenticationsViewsetView")
urlpatterns=[
    path('token/', CustomObtainAuthToken.as_view(), name='api-token'),
]

urlpatterns +=router.urls