from rest_framework.urls import path

from ModelViewSetApp.views import UploadDataModelViewsetView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"UploadDataByModelViewsetView",UploadDataModelViewsetView,basename="UploadDataByModelViewsetView")
urlpatterns=[

]

urlpatterns +=router.urls