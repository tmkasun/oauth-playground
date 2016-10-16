from django.conf.urls import url
from mock_api import views

urlpatterns = [
    url(r'^book$', views.books),
    url(r'^order$', views.order),
]
