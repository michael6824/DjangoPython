from django.shortcuts import render
from django.urls import reverse_lazy
# Create your views here.
import json
from asignaturas.models import *
from asignaturas.serializers import *
from rest_framework import generics
from django.views import generic
from asignaturas.forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

selectedperson = Persona()

class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class ProfesorList(generics.ListCreateAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer


class ProfesorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class AlumnoList(generics.ListCreateAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer


class AlumnoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class AsignaturaList(generics.ListCreateAPIView):
    queryset = AsignaturaModel.objects.all()
    serializer_class = AsignaturaSerializer


class AsignaturaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AsignaturaModel.objects.all()
    serializer_class = AsignaturaSerializer

class CartaDePagoList(generics.ListCreateAPIView):
    queryset = CartaDePago.objects.all()
    serializer_class = CartaDePagoSerializer


class CartaDePagoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartaDePago.objects.all()
    serializer_class = CartaDePagoSerializer

def post_list(request):
    if(request.method=="POST"):

        if(request.POST.get("Student","")!=""):

            return buildAsignature(request)
        else:

            if(request.POST.get("codeid","")!=""):

                return searchSecretaria(request)
            else:
                
                if(request.POST.get("NameAlumn","")!=""):

                    return AprobarSecretaria(request)
                else:
                    return buildcreate(request)

    else:
        return render(request, 'asignaturas/post_list.html', {})

def AprobarSecretaria(request):
    queryCarta = CartaDePago.objects.get(pk=(request.POST.get("codeeid","")))

    queryCarta.Aprobacion = True
    queryCarta.save()

    response_data ={}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def buildcreate(request):
    print("here")
    queryset = AsignaturaModel.objects.all()
    i=0
    student = Persona.objects.get(Name=(request.POST.get("Student","")))
    queryStudent = Alumno.objects.get(Persona=student)
    for x in queryset:

        test=request.POST.get("Code"+str(i),"")
        print(test)
        try:
            queryAsignature= AsignaturaModel.objects.get(Code=test)
            queryStudent.AsignaturasAlumno.add(queryAsignature)
        except:
            print("Not Found")

        i=i+1
    #print(queryStudent)
    response_data ={}

    try:
        response_data['result'] = 'success'
        response_data['message'] = test

    except:
        response_data['result'] = 'oh NO!'
        response_data['message'] = 'unsucessful'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def searchSecretaria(request):

    queryset = AsignaturaModel.objects.all()

    #queryStudent = Alumno.objects.get(Persona=student)
    response_data ={}
    try:
        queryCarta = CartaDePago.objects.get(pk=(request.POST.get("codeid","")))
        queryAlumno =Alumno.objects.get(CartaDePagoAlumno=queryCarta)
        response_data['result'] = 'Aprobado'
        response_data['name'] = queryAlumno.Persona.Name
    except:
        response_data['result'] = 'El número de recibo no pertenece a níngun Alumno'
        response_data['name']=""

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def AlumnoScreent(request,pk):


    #book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'asignaturas/AlumnoScreen.html',
        context={'Persona':pk,}
    )

class AlumnoScreen(generic.ListView):
    model = Alumno
    form_class = PersonaForm
    template_name = 'asignaturas/AlumnoScreen.html'
class ProfesorScreen(generic.DetailView):
    model = Profesor
    form_class = PersonaForm
    template_name = 'asignaturas/ProfesorScreen.html'
class SecretariaScreen(generic.ListView):
    model = Secretaria
    form_class = PersonaForm
    template_name = 'asignaturas/SecretariaScreen.html'

class AlumnosList(generic.ListView):
    model = Alumno
    form_class = PersonaForm
    template_name = 'asignaturas/test.html'



    def get_unsucess_url(self):

        return reverse_lazy('post_list')
    def post(self,request):
        #self.object = self.get_object

        Form1=PersonaForm(request.POST)

        try:
            queryperson = Persona.objects.get(Name=Form1['Name'].value())

            if(queryperson.Pin==Form1['Pin'].value()):


                query=queryperson.Position
                if(query==1):
                    try:
                        SelectedProfesor= Profesor.objects.get(Persona=queryperson)
                    except:
                        messages.warning(request, 'La Persona aún no está registrada como profesor.')
                        return HttpResponseRedirect(self.get_unsucess_url())
                #    MignaturaDeAlumno=(Alumno.objects.get(Persona=queryperson))

                    AsignaturaProfesor= AsignaturaModel.objects.filter(Profesor=SelectedProfesor)
                    #print(SelectedProfesor)
                    todas = AsignaturaModel.objects.all
                    return render(
                        request,
                        'asignaturas/ProfesorScreen.html',
                        context={'Persona':queryperson,'Asignatura':AsignaturaProfesor,'Todas':todas}
                    )
                elif(query==2):
                    try:
                        AsignaturaDeAlumno=(Alumno.objects.get(Persona=queryperson))
                        b1=(AsignaturaDeAlumno.AsignaturasAlumno.all)
                    except:
                        messages.warning(request, 'La Persona aún no está registrada como Alumno.')
                        return HttpResponseRedirect(self.get_unsucess_url())
                    return render(
                        request,
                        'asignaturas/AlumnoScreen.html',
                        context={'Persona':queryperson,'Asignatura':b1,}
                    )

                else:

                    try:
                        verify= Secretaria.objects.get(Persona=queryperson)
                    except:
                        messages.warning(request, 'La Persona aún no está registrada como Secretaria.')
                        return HttpResponseRedirect(self.get_unsucess_url())
                    return render(
                        request,
                        'asignaturas/SecretariaScreen.html',
                        context={'Persona':queryperson,}
                    )
            else:
                messages.warning(request, 'La contraseña es incorrecta.')
                return HttpResponseRedirect(self.get_unsucess_url())
        except:
            queryperson = "none"
            messages.warning(request, 'El nombre es incorrecto.')
            return HttpResponseRedirect(self.get_unsucess_url())
class RealizarMatricula(generic.CreateView):
    model = AsignaturaModel
    form_class = PersonaForm
    template_name = 'asignaturas/RealizarMatricula.html'

    def post(self, request):


        try:
            Form2=PersonaForm(request.POST)
            print(Form2['Name'].value())
            queryperson = Persona.objects.get(Name=Form2['Name'].value())
            queryalumn = Alumno.objects.get(Persona=queryperson)
            queryMatriculadas =queryalumn.AsignaturasAlumno.all


        except:
            print("Problem")
            queryperson=""
            queryalumn=""
            queryMatriculadas=""
        next = request.POST.get('next', '/')
        print(next)
        if(next!="/"):
            Form1=PersonaForm(request.POST)
        #    print(Form1)

            try:
                queryperson = Persona.objects.get(Name=Form1['Name'].value())
                print(Form1['Name'].value())
                AsignaturaDeAlumno=(Alumno.objects.get(Persona=queryperson))
                b1=(AsignaturaDeAlumno.AsignaturasAlumno.all)
            except:
                messages.warning(request, 'La Persona aún no está registrada como Alumno.')
                return HttpResponseRedirect(reverse_lazy('Asignatura-listar'))
            return render(
                            request,
                            'asignaturas/AlumnoScreen.html',
                            context={'Persona':queryperson,'Asignatura':b1,}
                        )

        else:
            return render(request, 'asignaturas/RealizarMatricula.html',context={'Persona':queryperson,'Matriculadas':queryMatriculadas,'Todas':AsignaturaModel.objects.all})


class AsignaturaCreate(generic.CreateView):
    model = AsignaturaModel
    form_class = PersonaForm
    template_name = 'asignaturas/CrearAsignatura.html'

    def post(self, request):

        Form2=PersonaForm(request.POST)

        try:
            print(Form2['Name'].value())
            queryperson = Persona.objects.get(Name=Form2['Name'].value())
            queryprofesor = Profesor.objects.get(Persona=queryperson)


        except:
            print("Problem")
            queryprofesor=""
        next = request.POST.get('next', '/')
        print(next)
        if(next!="/"):
            Form1=PersonaForm(request.POST)

            queryperson = Persona.objects.get(Name=Form1['Name'].value())

            SelectedProfesor= Profesor.objects.get(Persona=queryperson)

        #    MignaturaDeAlumno=(Alumno.objects.get(Persona=queryperson))

            AsignaturaProfesor= AsignaturaModel.objects.filter(Profesor=SelectedProfesor)
            #print(SelectedProfesor)
            todas=todas = AsignaturaModel.objects.all
            return render(
                request,
                'asignaturas/ProfesorScreen.html',
                context={'Persona':queryperson,'Asignatura':AsignaturaProfesor,'Todas':todas}
            )

        else:
            return render(
                            request,
                            'asignaturas/CrearAsignatura.html',
                            context={'Profesor':queryprofesor,}
                        )


def buildAsignature(request):

    queryset = AsignaturaModel.objects.all()
    i=0
    profesor = Profesor.objects.get(ProfesorID=(request.POST.get("Profesor","")))
    name =request.POST.get("Nombre","")
    code=request.POST.get("Code","")
    minsemester=request.POST.get("MinSemester","")
    #queryStudent = Alumno.objects.get(Persona=student)
    response_data ={}
    try:
        AsignaturaModel.objects.create(Name=name,Code=code,MinSemester=minsemester,Profesor=profesor)
        response_data['result'] = 'La Asignatura fue creada.'
    except:
        print("Not Created")
        response_data['result'] = 'El código ya existe.'




    return HttpResponse(json.dumps(response_data), content_type="application/json")



class MisEstudiantes(generic.CreateView):
    model = AsignaturaModel
    form_class = PersonaForm
    template_name = 'asignaturas/MisEstudiantes.html'

    def post(self, request):

        Form2=PersonaForm(request.POST)

        try:
            print(Form2['Name'].value())
            queryperson = Persona.objects.get(Name=Form2['Name'].value())
            queryprofesor = Profesor.objects.get(Persona=queryperson)


        except:
            print("Problem")
            queryprofesor=""
        next = request.POST.get('next', '/')
        print(next)
        if(next!="/"):
            Form1=PersonaForm(request.POST)

            queryperson = Persona.objects.get(Name=Form1['Name'].value())

            SelectedProfesor= Profesor.objects.get(Persona=queryperson)

        #    MignaturaDeAlumno=(Alumno.objects.get(Persona=queryperson))

            AsignaturaProfesor= AsignaturaModel.objects.filter(Profesor=SelectedProfesor)
            #print(SelectedProfesor)
            todas = AsignaturaModel.objects.all
            return render(
                request,
                'asignaturas/ProfesorScreen.html',
                context={'Persona':queryperson,'Asignatura':AsignaturaProfesor,'Todas': todas}
            )

        else:
            queryAsignature=AsignaturaModel.objects.get(id=request.POST.get('Name2'))
            queryList = Alumno.objects.filter(AsignaturasAlumno=queryAsignature)

            return render(
                            request,
                            'asignaturas/MisEstudiantes.html',
                            context={'Profesor':queryprofesor,'AsignaturaP':queryAsignature,'ListAsignaturas':queryList}
                        )
