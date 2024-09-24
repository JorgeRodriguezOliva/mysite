from .models import UserProfile, Region, Comuna, Inmueble, Solicitud, User


def get_or_create_user_profile(user):
    print(user.__dict__)
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            print("Se ha creado un nuevo perfil para el usuario.")
        else:
            print("El perfil ya existe")
        return user_profile
    except Exception as e:
        print(F'Error al obtener o crear el perfil del usuario. {e}')
        return None


def create_user(new_user):
    user = User.objects.create_user(
        username=new_user['username'],
        email=new_user['email'],
        first_name=new_user['first_name'],
        last_name=new_user['last_name'],
        password=new_user['password']
    )
    return user

def create_user_by_params(username,email,first_name,last_name,password):
    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    return user
# create_user_by_params("mau", "m@gmail.com", "mauro" .... ....)

def create_region(cod, nombre):
    region = Region(cod=cod, nombre=nombre)
    region.save()
    return region


def create_comuna(cod, nombre, cod_region):
    region = Region.objects.get(cod=cod_region)
    comuna = Comuna(cod=cod, nombre=nombre, cod_region=region)
    comuna.save()
    return comuna

def create_inmueble_for_arrendador(user, data):
    new_inmueble = Inmueble(**data)
    new_inmueble.arrendador = user 
    new_inmueble.save()
    return new_inmueble

def insertar_inmueble(data):
    arrendador = User.objects.get(id=data['arrendador'])
    comuna = Comuna.objects.get(cod=data['comuna'])
    inmueble = Inmueble(
        arrendador=arrendador,
        tipo_inmueble=data['tipo_inmueble'],
        comuna=comuna,
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        m2_construidos=data['m2_construidos'],
        m2_totales=data['m2_totales'],
        num_baños=data['num_baños'],
        num_habitaciones=data['num_habitaciones'],
        num_estacionamientos=data.get('num_estacionamientos', 0),
        direccion=data['direccion'],
        precio=data.get('precio', None),
        precio_ufs=data.get('precio_ufs', None)
    )
    inmueble.save()
    return inmueble


def get_all_inmuebles():
    # inmuebles = Inmueble.objects.all()
    try:
        inmueble= Inmueble.objects.filter(disponible=True)
        return inmueble
    except Exception as e:
        print(f"Error al obtener los inmuebles: {str(e)}")
        return []


def actualizar_disponibilidad_inmueble(id_inmueble, disponible):
    try:
        inmueble = Inmueble.objects.get(pk=id_inmueble)
        inmueble.disponible = disponible
        inmueble.save()
        return {
            "success": True,
            "message": "Disponibilidad actualizada con éxito"
        }
    except Inmueble.DoesNotExist:
        return {
            "success": False,
            "message": "Inmueble no encontrado"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al actualizar la disponibilidad del inmueble: {str(e)}"
        }


def eliminar_inmueble(id_inmueble):
    try:
        inmueble = Inmueble.objects.get(pk=id_inmueble)
        inmueble.delete()
        return {
            "success": True,
            "message": "Inmueble eliminado con éxito"
        }
    except Inmueble.DoesNotExist:
        return {
            "success": False,
            "message": "Inmueble no encontrado"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al eliminar el inmueble: {str(e)}"
        }
        
def get_inmuebles_for_arrendador(user):
    rol = user.userprofile.rol 
    if rol != 'arrendador':
        print(f'no es arrendador')
        return [] 
    inmuebles = Inmueble.objects.filter(arrendador=user)
    if not inmuebles.exists():
        print(f'no hay inmuebles')
        return []
    return inmuebles
