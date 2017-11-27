import django.conf.urls

from . import views

app_name = 'updater'
urlpatterns = [
    django.conf.urls.url(r'^$', views.greetings, name='greetings'),
    # Returns the update file list.
    django.conf.urls.url(r'^file_list/$', views.FileListView.as_view(), name='file_list'),
    # Must receive a post request containing the missing files.
    django.conf.urls.url(r'^fire_sending/$', views.MissingFileView.as_view(), name='fire_sending'),
]
