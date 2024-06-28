from rest_framework.urls import path

from ViewSetApp.views import UploadDataViewsetView
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r"UploadDataByViewsetView",UploadDataViewsetView)
urlpatterns=[

]
urlpatterns +=router.urls