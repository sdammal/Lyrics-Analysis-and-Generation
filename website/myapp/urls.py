from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name='landing_page'),

    path('about', views.about_page, name='about'),

    path('analysis_homepage', views.analysis_homepage, name='analysis_homepage'),
    path('analysis/<str:artist_name>/', views.analysis, name='analysis'),

    path('generate', views.generate_lyrics, name='generate_lyrics'),

    path('vocals', views.generate_vocals, name='generate_vocals'),

]