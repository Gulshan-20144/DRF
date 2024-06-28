from django.urls import path,include

from SessionAuthenticationApp.views import  SessionAuthenticationsViewsetView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"SessionAuthenticationsViewsetView",SessionAuthenticationsViewsetView,basename="SessionAuthenticationsViewsetView")
urlpatterns=[
   path('', include("rest_framework.urls"), name='login'),
]
urlpatterns +=router.urls