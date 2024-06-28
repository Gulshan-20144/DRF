from rest_framework.urls import path
from ApiViewApp.views import UploadDataView

urlpatterns = [
    path("ApiViewData/",UploadDataView.as_view(),name="ApiViewData"),
    path("ApiViewData/list/",UploadDataView.as_view(),name="ApiViewData"),
    path("ApiViewData/get/<int:pk>/",UploadDataView.as_view(),name="ApiViewData"),
    path("ApiViewData/patch/<int:pk>/",UploadDataView.as_view(),name="ApiViewData"),
    path("ApiViewData/delete/<int:pk>/",UploadDataView.as_view(),name="ApiViewData")
]
