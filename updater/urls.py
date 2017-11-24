import django.conf.urls

from . import views

app_name = 'updater'
urlpatterns = [
    django.conf.urls.url(r'^$', views.greetings, name='greetings'),
    django.conf.urls.url(r'^file_list/$'),
    # Get missing files with post request.
    django.conf.urls.url(r'^fire_sending/$'),
]
