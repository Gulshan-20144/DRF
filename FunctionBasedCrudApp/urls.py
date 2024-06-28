from rest_framework.urls import path
from FunctionBasedCrudApp.views import bookstore_list,bookstore_detail,bookstore_create,bookstore_partial_update

urlpatterns = [
    path("list_data/",bookstore_list,name="list_data"),
    path("add_daat/create/",bookstore_create,name="add_daat"),
    path("reteriev_details/get/<int:pk>/",bookstore_detail,name="reteriev_details"),
    path("update_data/patch/<int:pk>/",bookstore_partial_update,name="update_data")
]
