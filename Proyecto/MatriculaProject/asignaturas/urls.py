from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from asignaturas import views
from django.urls import path

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('hi', views.ProfesorScreen, name='ProfesorScreen'),
    #path('/', views.buildAsignature, name='buildAsignature'),
#    path('test/testcreate/', views.AsignaturaCreate, name='AsignaturaCreate'),
    url(r'^AlumnoScreen/1', views.AlumnoScreen.as_view(),name='AlumnoScreen'),
    #url(r'^ProfesorScreen/1', views.ProfesorScreen.as_view(),name='ProfesorScreen'),
    url(r'^SecretariaScreen/1', views.SecretariaScreen.as_view(),name='SecretariaScreen'),
    url(r'^test/RealizarMatricula/?', views.RealizarMatricula.as_view(),name='RealizarMatricula'),
    url(r'^test/MisEstudiantes/?', views.MisEstudiantes.as_view(),name='MisEstudiantes'),
    url(r'^Persona/$', views.PersonaList.as_view()),
    url(r'^Persona/1', views.PersonaDetail.as_view()),
    url(r'^Profesor/$', views.ProfesorList.as_view()),
    url(r'^Profesor/1', views.ProfesorDetail.as_view()),
    url(r'^Alumno/$', views.AlumnoList.as_view(),name="Alumno-listar"),
    url(r'^Alumno/1', views.AlumnoDetail.as_view()),
    url(r'^Asignatura/$', views.AsignaturaList.as_view()),
    url(r'^Asignatura/1', views.AsignaturaDetail.as_view()),
    url(r'^CartaDePago/$', views.CartaDePagoList.as_view()),
    url(r'^CartaDePago/1', views.CartaDePagoDetail.as_view()),
    url(r'^test/$', views.AlumnosList.as_view(),name="Asignatura-listar"),
    url(r'^test/testcreate/?', views.AsignaturaCreate.as_view(),name='AsignaturaCreate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
