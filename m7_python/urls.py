from django.urls import path
from .views import (indexView, register, register_rol, profile_view, profile_edit, edit_status_solicitud,
                    profile_exito, about,contact, index_arrendatario, dashboard_arrendador,
                    create_inmueble,edit_inmueble,detail_inmueble,delete_inmueble, view_list_solicitudes,
                    edit_disponibilidad_inmueble,send_solicitud, view_list_user_solicitudes, cancelar_solicitud)

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
    
    path('index', index_arrendatario, name='index_arrendatario'),
    path('inmueble/solicitar/<int:inmueble_id>/', send_solicitud, name='send_solicitud'),
    path('list/solicitudes/', view_list_user_solicitudes, name='solicitudes'),
    path('cancelar_solicitud/<int:solicitud_id>/', cancelar_solicitud, name='cancelar_solicitud'),
    
    path('dashboard', dashboard_arrendador, name="dashboard_arrendador"),
    path('dashboard/create', create_inmueble, name="create_inmueble"),
    path('dashboard/inmueble/edit/<int:inmueble_id>/',edit_inmueble, name='edit_inmueble'),
    path('dashboard/detail/<int:inmueble_id>/', detail_inmueble, name="detail_inmueble"),
    path('dashboard/inmueble/delete/<int:inmueble_id>/',delete_inmueble, name='delete_inmueble'),
    path('dashboard/inmueble/disponibilidad/<int:inmueble_id>/', edit_disponibilidad_inmueble, name='edit_disponibilidad_inmueble'),
    path('dashboard/inmueble/solicitudes/<int:inmueble_id>/', view_list_solicitudes, name='view_list_solicitudes'),
    path('dashboard/solicitud/edit-status/<int:solicitud_id>/', edit_status_solicitud, name='edit_status_solicitud'),
    

]
