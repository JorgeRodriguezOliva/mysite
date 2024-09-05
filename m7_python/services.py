from django.contrib.auth.models import User
from m7_python.models import UserProfile,Region,Comuna,Inmueble,Solicitud

def create_user(new_user):
    user = User.objects.create_user(
        username=new_user['username'],
        email=new_user['email'],
        first_name=new_user['first_name'],
        last_name=new_user['last_name'],
        password=new_user['password']
    )
    return user

def create_region(cod,nombre):
    region=Region(cod=cod,nombre=nombre)
    region.save()
    return region

def create_comuna(cod,nombre,cod_region)
    region=Region.objects.get(cod=cod_region)
    comuna=Comuna(cod=cod,nombre=nombre,cod_region=region)
    comuna.save()
    return comuna

def insertar_inmueble(data):
    arrendador = User.objects.get(id=data['id_user'])
    comuna = Comuna.objects.get(cod=data['comuna_cod'])
    inmueble=Inmueble(
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
    inmuebles = Inmueble.objects.all()
    return inmuebles

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
