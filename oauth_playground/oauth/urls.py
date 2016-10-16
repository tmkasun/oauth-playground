from django.conf.urls import url
from oauth import views

urlpatterns = [
    url(r'^submit', views.submit),
    url(r'^callback', views.callback),
    url(r'^access_token', views.request_access_token),
    url(r'^request_resource', views.request_resource)
]
