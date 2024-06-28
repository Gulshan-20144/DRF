from rest_framework.urls import path

from GenricViewSetApp.views import UploadDataGenricViewsetView
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r"UploadDataByGenricViewsetView",UploadDataGenricViewsetView)
urlpatterns=[

]
urlpatterns +=router.urls