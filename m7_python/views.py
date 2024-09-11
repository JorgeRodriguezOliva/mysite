from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .services import get_all_inmuebles, get_or_create_user_profile
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, UserEditProfileForm, UserForm, ContactModelForm
from .models import UserProfile, ContactForm
from django.contrib.auth import login

@login_required
def indexView(req):
    inmuebles = get_all_inmuebles()
    return render(req, 'index.html', {'inmuebles': inmuebles})

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
    # Verificar que el User tiene un Perfil
    user_id = request.user.id
    print(f'id {user_id} {request.user.first_name}')
    user = request.user
    user_profile = get_or_create_user_profile(user)  
    # * User de no tener un Profile, crea la relación
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user_id=user_id)
        print(f'user profile get -> {profile.__dict__}')
    # * ARMADO POST - crea (guarda en la tabla) - y redirect
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserEditProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Redirigir a la misma página después de guardar
            return redirect('/profile_exito')
    # * GET FORM - Creamos los forms con los datos de la DB de ese user
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

def contact(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/profile_exito')
    else:
        form = ContactModelForm()
    return render(request, 'contact.html', {'form': form})
