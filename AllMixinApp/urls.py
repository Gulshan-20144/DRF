from rest_framework.urls import path

from AllMixinApp.views import AllMixinAppView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"AllMixinurl",AllMixinAppView,basename="AllMixinurl")
urlpatterns=[

]

urlpatterns +=router.urls