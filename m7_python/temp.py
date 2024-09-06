import os
import django
from decouple import config
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mysite
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from m7_python.models import Inmueble, Region, Comuna
from django.contrib.auth.models import User

def listado_inmuebles_comuna_orm(comuna, descr=None):
    filtros = {
            'comuna__nombre__icontains': comuna
    }
    if descr:
        filtros['descripcion__icontains'] = descr
        
    inmuebles = Inmueble.objects.filter(**filtros)
    index=1
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n__ listado_inmuebles_comuna_orm __\n')
        for l in inmuebles:
            file.write(f"{index}__ Nombre: [{l.nombre}], Descripción:[{l.descripcion}] \t\tComuna: {l.comuna.nombre}\n")
            index += 1
    return

def listado_inmuebles_comuna_sql(comuna):
    select = """
    SELECT A.id, A.nombre AS nombre_inmueble, A.descripcion
    FROM m7_python_inmueble A
    INNER JOIN m7_python_comuna C ON A.comuna_id = C.cod
    WHERE C.nombre ILIKE %s
    """
    inmuebles = Inmueble.objects.raw(select, [f"%{comuna}%"])
    index=1
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n __ listado_inmuebles_comuna_sql __\n')
        for l in inmuebles:
            file.write(f"{index}__ Nombre: [{l.nombre}], Descripción:[{l.descripcion}] \t\tComuna: {l.comuna.nombre}\n")
            index += 1
    return

def listado_inmuebles_region_orm(region,descr=None):
    filtros = {
            'comuna__region__nombre__icontains': region
    }
    if descr:
        filtros['descripcion__icontains'] = descr
    
    inmuebles = Inmueble.objects.filter(**filtros)
    index=1
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n__ listado_inmuebles_region_orm __\n')
        for l in inmuebles:
            file.write(f"{index}__ Nombre: [{l.nombre}], Descripción:[{l.descripcion}] \t\tRegión: {l.comuna.region.nombre}\n")
            index += 1
    return

def listado_inmuebles_region_sql(region):
    select = """
    SELECT A.id, A.nombre AS nombre_inmueble, A.descripcion
    FROM m7_python_inmueble A
    INNER JOIN m7_python_comuna C ON A.comuna_id = C.cod
    INNER JOIN m7_python_region R ON C.region_id=R.cod
    WHERE R.nombre ILIKE %s
    """
    inmuebles = Inmueble.objects.raw(select, [f"%{region}%"])
    index=1
    with open("m7_python/outputs/datos.txt", "a") as file:
        file.write(f'\n __ listado_inmuebles_region_sql __\n')
        for l in inmuebles:
            file.write(f"{index}__ Nombre: [{l.nombre}], Descripción:[{l.descripcion}] \t\tRegión: {l.comuna.region.nombre}\n")
            index += 1
    return


if __name__ == "__main__":
    # TODO_ Ejemplos SIMPLES:
    listado_inmuebles_comuna_orm('pucón')
    listado_inmuebles_comuna_sql('Ovalle')
    listado_inmuebles_region_orm('Del Biobío')
    listado_inmuebles_region_sql('De Valparaíso')


