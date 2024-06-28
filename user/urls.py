from django.urls import path
from .views import *

urlpatterns=[
    path("reagister/",RagistrationsApiView.as_view()),
    path("Obtaintoken/",LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]
