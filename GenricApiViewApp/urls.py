from rest_framework.urls import path
from GenricApiViewApp.views import UploadDataView

urlpatterns = [
    path("GenricsApiViewData/",UploadDataView.as_view(),name="ApiViewData"),
    path("GenricsApiViewData/list/",UploadDataView.as_view(),name="ApiViewData"),
    path("GenricsApiViewData/get/<int:pk>/",UploadDataView.as_view(),name="ApiViewData"),
    path("GenricsApiViewData/patch/<int:pk>/",UploadDataView.as_view(),name="ApiViewData"),
    path("GenricsApiViewData/destroy/<int:pk>/",UploadDataView.as_view(),name="ApiViewData")
]
