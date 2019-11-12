from django.contrib import admin

# Register your models here.
from asignaturas.models import *

admin.site.register(Persona)
admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(Secretaria)
admin.site.register(CartaDePago)
admin.site.register(AsignaturaModel)
admin.site.register(Notas)
