from django.contrib import admin
from django.urls import path
from .views import indexView
from .services import get_all_inmuebles
# from . import views


urlpatterns = [
    path('',indexView,name='home')

]