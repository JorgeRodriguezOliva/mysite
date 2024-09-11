from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.

class UserProfile(models.Model):
    ROLES = (('arrendador', 'Arrendador'), ('arrendatario', 'Arrendatario'))
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    rut = models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=255, choices=ROLES, default='arrendatario')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.rol}'


class Region(models.Model):
    cod = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre} ({self.cod})'


class Comuna(models.Model):
    cod = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=255)
    region = models.ForeignKey(
        Region, on_delete=models.RESTRICT, related_name='comunas')

    def __str__(self):
        return f'{self.nombre} ({self.cod})'


class Inmueble(models.Model):
    TIPO = (('casa', 'Casa'), ('bodega', 'Bodega'),
            ('departamento', 'Departamento'), ('parcela', 'Parcela'))
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1500)
    m2_construidos = models.IntegerField(validators=[MinValueValidator(1)])
    m2_totales = models.IntegerField(validators=[MinValueValidator(1)])
    num_estacionamientos = models.IntegerField(
        validators=[MinValueValidator(0)], default=0)
    num_habitaciones = models.IntegerField(
        validators=[MinValueValidator(1)], default=1)
    num_baños = models.IntegerField(
        validators=[MinValueValidator(0)], default=0)
    direccion = models.CharField(max_length=255)
    tipo_inmueble = models.CharField(max_length=50, choices=TIPO)
    precio = models.IntegerField(
        validators=[MinValueValidator(1000)], null=True)
    precio_ufs = models.FloatField(
        validators=[MinValueValidator(1.0)], null=True)
    disponible = models.BooleanField(default=True)
    comuna = models.ForeignKey(
        Comuna, related_name='inmuebles', on_delete=models.RESTRICT)
    arrendador = models.ForeignKey(
        User, related_name='inmuebles', on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.nombre} {self.descripcion} {self.comuna.region.nombre}'


class Solicitud(models.Model):
    ESTADOS = (('pediente', 'Pendiente'), ('rechazada', 'Rechazada'),
            ('aprobada', 'Aprobada'), ('finalizada', 'Finalizada'))
    inmueble = models.ForeignKey(
        Inmueble, related_name='solicitudes', on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(
        User, related_name='solicitudes_arrendatario', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=50, choices=ESTADOS, default='pendiente')
    
class ContactForm(models.Model):
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
    
    def __str__(self):
        return self.customer_name
