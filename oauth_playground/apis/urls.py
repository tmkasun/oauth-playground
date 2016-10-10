from django.conf.urls import url
from apis import views

urlpatterns = [
    url(r'^submit$', views.submit)
]
