from django.urls import path
from . import views

urlpatterns = [
    path('bot/home/', views.bothome, name='bothome'),
    path('start/first/bot/', views.startbotone, name='startbotone'),
    path('second/bot/initiate/', views.startbottwo, name='startbottwo'),
    path('all/bot/done/', views.startbotthree, name='startbotthree'),
    path('', views.home, name='home'),
    path('blogs', views.post_list, name='blog'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('sermons', views.Sermon_list, name='sermons'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.Sermons_detail,
         name='sermon_detail'),
    path('events', views.Events_list, name='events'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.Events_detail,
         name='post_detail'),

]
