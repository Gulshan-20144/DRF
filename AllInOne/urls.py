"""
URL configuration for AllInOne project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from SerializersApp.urls import router as Sr
schema_view = get_schema_view(
    openapi.Info(
        title="DRF SWAGGER",
        default_version='1.0.0',
        description="API Description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('user.urls')),
    path('api/',include('ModelSerializersApp.urls')),
    path('api/',include('HyperLinkSerializersApp.urls')),
    path('api/',include('BaseSerializersApp.urls')),
    path('api/ListSerializersApp',include('ListSerializersApp.urls')),
    path('api/',include('ApiViewApp.urls')),
    path('api/',include('GenricApiViewApp.urls')),
    path('api/v1/',include('ViewSetApp.urls')),
    path('api/',include('ModelViewSetApp.urls')),
    path('api/',include('GenricViewSetApp.urls')),
    path('api/',include('AllMixinApp.urls')),
    path('api/',include('RouterApp.urls')),
    path('api/',include('BasicAuthenticationsApp.urls')),
    path('api/',include('TokenAuthenticationApp.urls')),
    path('api/',include('SessionAuthenticationApp.urls')),
    path('api/',include('JwtAuthenticationApp.urls')),
    path('api/',include('FunctionBasedCrudApp.urls')),
    path('api/',include('OAuthBasedAuthentications.urls')),
    path('api/schema', schema_view.with_ui(), name='schema'),
    path('api/doc', schema_view.with_ui('swagger',cache_timeout=0), name='swagger-ui'),
]

urlpatterns +=Sr.urls