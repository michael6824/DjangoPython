from rest_framework import serializers
from asignaturas.models import *
from .utils import CustomerTypes



class ProfesorSerializer(serializers.ModelSerializer):
    Persona= serializers.PrimaryKeyRelatedField(queryset=Persona.objects.filter(Position=CustomerTypes.Profesor))
    class Meta:
        model = Profesor
        fields = ('id', 'Persona', 'ProfesorID')

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'Name', 'LastName', 'Phone', 'Pin','DNI','Position')

class SecretariaSerializer(serializers.ModelSerializer):
    Persona= serializers.PrimaryKeyRelatedField(queryset=Persona.objects.filter(Position=CustomerTypes.Secretaria))
    class Meta:
        model = Secretaria
        fields = ('id','Persona','CartaDePago')

class AlumnoSerializer(serializers.ModelSerializer):
    Persona= serializers.PrimaryKeyRelatedField(queryset=Persona.objects.filter(Position=CustomerTypes.Alumno))

    class Meta:
        model = Alumno
        fields = ('id','Persona','Semester','AsignaturasAlumno','CartaDePagoAlumno')
class CartaDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaDePago
        fields = ('id','Precio','Aprobacion')
class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignaturaModel
        fields = ('id', 'Name','Code','MinSemester','Profesor')
