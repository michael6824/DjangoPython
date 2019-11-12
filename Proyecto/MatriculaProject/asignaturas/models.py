from django.db import models
from .utils import CustomerTypes
# Create your models here.
class Persona(models.Model):
    Name = models.CharField(max_length=100, blank=True, default='')
    LastName = models.CharField(max_length=100, blank=True, default='')
    Phone = models.IntegerField()
    Pin = models.CharField(max_length=4)
    DNI = models.CharField(max_length=20, blank=True, default='')
    Position = models.IntegerField(choices=CustomerTypes.choices(), default=CustomerTypes.Profesor)
    class Meta:
        ordering = ('Name',)

class Profesor(models.Model):
    Persona = models.OneToOneField(Persona, on_delete=models.CASCADE, limit_choices_to={'Position':CustomerTypes.Profesor})
    ProfesorID = models.CharField(max_length=4, blank=True, default='')
    class Meta:
        ordering = ('Persona',)
class AsignaturaModel(models.Model):
    Name = models.CharField(max_length=100, blank=True, default='')
    Code = models.CharField(max_length=100, blank=True, default='',unique=True)
    MinSemester = models.IntegerField()
    Profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    class Meta:
        ordering = ('Name',)



class CartaDePago(models.Model):
    Precio = models.CharField(max_length=100, blank=True, default='')
    Aprobacion = models.BooleanField(blank=True, default=False)
    class Meta:
        ordering = ('Aprobacion',)

class Alumno(models.Model):
    Persona = models.OneToOneField(Persona, on_delete=models.CASCADE, limit_choices_to={'Position':CustomerTypes.Alumno})
    Semester = models.IntegerField()

    AsignaturasAlumno = models.ManyToManyField(AsignaturaModel)
    CartaDePagoAlumno = models.ForeignKey(CartaDePago, on_delete=models.CASCADE)
    class Meta:
        ordering = ('Persona',)

class Notas(models.Model):
    Nota= models.IntegerField()
    UniqueAlumn= models.ForeignKey(Alumno,on_delete=models.CASCADE,)
    UniqueAsignature =models.ForeignKey(AsignaturaModel,on_delete=models.CASCADE,)

    class Meta:
        ordering = ('Nota',)

class Secretaria(models.Model):
    Persona = models.OneToOneField(Persona, on_delete=models.CASCADE,limit_choices_to={'Position':CustomerTypes.Secretaria})
    CartasDePago = models.ManyToManyField(CartaDePago)
    class Meta:
        ordering = ('Persona',)
