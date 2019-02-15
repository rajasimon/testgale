from django.urls import path

from testgale.core import views

app_name='core'
urlpatterns = [
    path('', views.index, name='index'),
    path('crawl/', views.crawl, name='crawl')
]
