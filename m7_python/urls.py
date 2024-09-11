from django.urls import path
from .views import indexView, register, register_rol, profile_view, profile_edit, profile_exito, about,contact

# from . import views


urlpatterns = [
    path('', indexView, name='home'),
    path('accounts/register', register, name='register'),
    path('accounts/register_rol', register_rol, name='register_rol'),
    path('profile', profile_view, name='profile'),
    path('profile_edit', profile_edit, name='profile_edit'),
    path('profile_exito', profile_exito, name='profile_exito'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
]
