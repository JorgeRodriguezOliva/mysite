from django.shortcuts import render, redirect, get_object_or_404
from .services import get_all_inmuebles, get_or_create_user_profile, get_inmuebles_for_arrendador, insertar_inmueble,create_inmueble_for_arrendador,actualizar_disponibilidad_inmueble
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, UserEditProfileForm, UserForm, ContactModelForm,InmuebleForm, EditDisponibilidadForm
from .models import UserProfile, ContactForm, Region,Comuna, Inmueble, User, Solicitud
from django.contrib.auth import login
from django.contrib import messages
# from django.http import HttpResponse, HttpResponseRedirect
from .decorators import rol_requerido

#* Route para manejo de NOT_AUTH
def not_authorized_view(request):
    return render(request, "not_authorized.html", {})

@login_required
def indexView(request):
    if request.user.is_authenticated:
        profile = get_or_create_user_profile(request.user)
        if profile.rol == 'arrendador':
            messages.success(request, 'GENIAL!!!')
            return redirect('dashboard_arrendador')
        elif profile.rol == 'arrendatario':
            return redirect('index_arrendatario')
        else: 
            return redirect('login')
    else:
        return redirect('login')

@login_required   
def index_arrendatario(request):
    inmuebles = get_all_inmuebles()
    return render(request,'arrendatario/index_arrendatario.html',{'inmuebles':inmuebles} )

@login_required 
def dashboard_arrendador(request):
    inmuebles = get_inmuebles_for_arrendador(request.user)
    return render(request, 'arrendador/dashboard_arrendador.html', {'inmuebles': inmuebles})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register_rol')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def register_rol(request):
    user_profile = get_or_create_user_profile(request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'registration/register_rol.html', {'form': form})

#* VER PERFIL
@login_required
def profile_view(request):
    user = request.user
    user_profile = get_or_create_user_profile(user)  
    if not user_profile:
        return render(request, 'error.html', {'message': 'No se pudo obtener el perfil del usuario.'})
    return render(request, 'profile_detail.html', {
        'user': user,
        'profile': user_profile,
    })

@login_required
def profile_edit(request):
    user_id = request.user.id
    print(f'id {user_id} {request.user.first_name}')
    user = request.user
    user_profile = get_or_create_user_profile(user)  
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user_id=user_id)
        print(f'user profile get -> {profile.__dict__}')
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserEditProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile_exito')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserEditProfileForm(instance=user_profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile':user_profile,
    })
    
def profile_exito(request):
    return render(request, 'profile_exito.html', {})


def about(request):
    return render(request, 'about.html', {})

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        print(f'errors -> {form.errors}')
        if form.is_valid():
            ContactForm.objects.create(**form.cleaned_data)
            return redirect('/profile_exito')
    else:
        form = ContactModelForm()
    return render(request, 'contact.html', {'form': form})
#___________________________________________________________________________________________________
#███████████████████████████████████████████████████████████████████████████████████████████████████
#TODO__ ARRENDADOR - VIEWS

#* HITO 4
@login_required
@rol_requerido('arrendador')
def create_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = create_inmueble_for_arrendador(request.user, form.cleaned_data)
            return redirect('dashboard_arrendador')
    else: 
        form = InmuebleForm()
    return render(request, 'arrendador/create_inmueble.html', {'form': form})


# @login_required
# @rol_requerido('arrendador')
def create_inmueble2(request):
    regiones = Region.objects.all()
    comunas = Comuna.objects.all().order_by('nombre')
    tipos_inmuebles = Inmueble.TIPO # Tipos de inmuebles
    print(tipos_inmuebles)
    
    context = {
        'regiones': regiones,
        'comunas': comunas,
        'tipos_inmuebles': tipos_inmuebles
    }
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        m2_construidos = int(request.POST['m2_construidos'])
        m2_totales = int(request.POST['m2_totales'])
        num_estacionamientos = int(request.POST['num_estacionamientos'])
        num_habitaciones = int(request.POST['num_habitaciones'])
        num_baños = int(request.POST['num_baños'])
        direccion = request.POST['direccion']
        precio_mensual_arriendo = int(request.POST['precio_mensual_arriendo'])
        tipo_de_inmueble = request.POST['tipo_de_inmueble']
        comuna_cod = request.POST['comuna_cod']
        rut_propietario = request.user

        crear = insertar_inmueble(nombre, descripcion, m2_construidos, m2_totales, num_estacionamientos, num_habitaciones, num_baños, direccion, precio_mensual_arriendo, tipo_de_inmueble, comuna_cod, rut_propietario)
        if crear: # Si return render(request, 'add_propiedad.html', context)crear es True
            messages.success(request, 'Propiedad ingresada con éxito')
            return redirect('profile')
        # Si llega aquí, es porque crear fue False
        messages.warning(request, 'Hubo un problema al crear la propiedad, favor revisar')
        return render(request, 'crear_inmueble.html', context)
    else: 
        return render(request, 'crear_inmueble.html', context)


# def create_inmueble(request):
#     pass

@login_required
def edit_inmueble(request, inmueble_id):
    inmueble_edit =  get_object_or_404(Inmueble, id=inmueble_id)
    # inmueble_edit =  Inmueble.objects.get(pk=inmueble_id)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble_edit)
        if form.is_valid():
            #* Crear service para update Inmueble y validar
            form.save()
            return redirect('dashboard_arrendador')
    else: 
        form = InmuebleForm(instance=inmueble_edit)
    return render(request, 'arrendador/edit_inmueble.html', {'form': form})

@login_required
def delete_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        inmueble.delete()
        return redirect('dashboard_arrendador')

    return render(request, 'arrendador/delete_inmueble.html', {'inmueble': inmueble})


@login_required
def detail_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    # inmueble =  Inmueble.objects.get(id=inmueble_id)
    return render(request, 'detail_inmueble.html', {'inmueble': inmueble})

@login_required
def edit_disponibilidad_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        form = EditDisponibilidadForm(request.POST, instance=inmueble) 
        if form.is_valid():
            disponible = form.cleaned_data['disponible']
            result = actualizar_disponibilidad_inmueble(inmueble_id, disponible)
            if result["success"]:
                messages.success(request, result["message"])
            else: 
                messages.error(request, result["message"])
            return redirect('dashboard_arrendador')
    else: 
        form = EditDisponibilidadForm(instance=inmueble)
    return render(request, 'arrendador/edit_disponibilidad.html', {'form': form, 'inmueble': inmueble})

#___________________________________________________________________________________________________
#███████████████████████████████████████████████████████████████████████████████████████████████████
#TODO__ ARRENDATARIOS - VIEWS


@login_required
@rol_requerido('arrendatario')
def send_solicitud(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    if request.method == 'POST':
        solicitud = Solicitud(arrendatario= request.user, inmueble= inmueble, estado= 'pendiente')
        solicitud.save()
        messages.success(request, f'Solicitud inmueble {inmueble.nombre} realizada con éxito!!!')
        return redirect('index_arrendatario')
    return render(request, 'arrendatario/send_solicitud.html', {'inmueble': inmueble})
    
    


def view_list_user_solicitudes(request):
    
    arrendatario =  get_object_or_404(User, id=request.user.id)
    solicitudes = Solicitud.objects.filter(arrendatario=arrendatario)
    return render(request, 'arrendatario/list_user_solicitudes.html', {
        'solicitudes': solicitudes,
        'arrendatario': arrendatario
    })

#*___________________________________________HITO 4 FIN *****************

#* DAY 19 HITO 5 - MARTES

#* del ARRENDADOR
@login_required
def view_list_solicitudes(request, inmueble_id):
    pass 

@login_required
def edit_status_solicitud(request, solicitud_id):
    pass 

def cancelar_solicitud(request, solicitud_id):
    pass 
#! Estas van a ser funciones (services)
#* x REGION y x COMUNA
def filtros(request):
    pass 

def buscar_por_nombre(request):
    pass


