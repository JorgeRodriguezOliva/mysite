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


# def listado_inmuebles_comuna_orm(comuna):
#     inmuebles=Inmueble.objects.filter(comuna__nombre__icontains=comuna)
#     index=1
#     print("LISTA INMUEBLES")
#     for l in inmuebles:
#         print(f"{index}__ {l.nombre}, {l.descripcion}- comuna: {l.comuna.nombre}\n")
#         index += 1
#     with open("m7_python/outputs/datos.txt", "a") as file:
#         for l in inmuebles:
#             file.write(f" {l.nombre}, {l.descripcion} - comuna: {l.comuna.nombre}\n")
#     return

# def get_list_inmuebles_sql():
#     select = """
#         SELECT * FROM m7_python_inmueble
#         """
#     inmuebles = Inmueble.objects.raw(select)
#     index=1
#     print("LISTA INMUEBLES")
#     for l in inmuebles:
#         print(f"{index}__ {l.nombre}, {l.descripcion}")
#         index += 1
#     with open("m7_python/outputs/datos.txt", "a") as file:
#         for l in inmuebles:
#             file.write(f" {l.nombre}, {l.descripcion}\n")
#     return
# if __name__ == "__main__":
#     #TODO_ Ejemplos SIMPLES:
#     get_list_inmuebles_sql()


# def listado_inmuebles_comuna_sql():
#     select = """
#         select m7_python_inmueble.nombre from m7_python_inmueble
#         """
#     inmuebles = Inmueble.objects.raw(select)
#     index = 1
#     print("LISTA INMUEBLES")
#     for l in inmuebles:
#         print(l)

    # print(f"{index}__ {l.comuna}, {l.nombre}__{l.descripcion}")
    #index += 1
    # with open("m7_python/outputs/datos.txt", "a") as file:
    #     for l in inmuebles:
    #         file.write(f" {l.comuna}, {l.nombre}__{l.descripcion}\n")
    #return