from rest_framework.urls import path
from django.urls import re_path, include

from RouterApp.views import RouterDataView,UploadDataRouterView,RouterApiView,DistibuterView
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r"RouterBooksUrls",UploadDataRouterView),
router.register(r"DistibuterUrls",DistibuterView)
urlpatterns=[
    re_path(r"^",include(router.urls)),
    re_path(r'^AllBooks/$', RouterDataView.as_view(), name="AllBooks-list"),
    re_path(r'^Booksby/(?P<pk>[0-9]+)/$', RouterDataView.as_view(), name="AllBooks-detail"),
    path("RouterGetData/list/",RouterApiView.as_view(),name="RouterApiView"),
    path("RouterGetDatabyId/get/<int:pk>/",RouterApiView.as_view(),name="RouterApiView"),
    path("RouterGetDatabyIdupdate/patch/<int:pk>/",RouterApiView.as_view(),name="RouterApiView"),
    
]
urlpatterns +=router.urls