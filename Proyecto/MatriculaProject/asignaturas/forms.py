from django import forms
from asignaturas.models import *

class AsignaturaForm(forms.ModelForm):

    class Meta:
        model= AsignaturaModel

        fields = [
            'Name',
            'Code',
            'MinSemester',
            'Profesor',
            ]
        labels = {
            'Name':'name',
            'Code':'code',
            'MinSemester':'minsemester',
            'Profesor':'profesor',
        }

        widgets = {
            'Name':forms.TextInput(attrs={'class':'form-control'}),
            'Code':forms.TextInput(attrs={'class':'form-control'}),
            'MinSemester':forms.NumberInput(attrs={'class':'form-control'}),
            'Profesor':forms.Select(attrs={'class':'form-control'}),
        }

class PersonaForm(forms.ModelForm):


    class Meta:
        model= Persona

        fields = [
            'Name',
            'Pin',
            ]
        labels = {
            'Name':'name',
            'Pin':'pin',
            }

        widgets = {
            'Name':forms.TextInput(attrs={'class':'form-control'}),
            'Pin':forms.TextInput(attrs={'class':'form-control'}),

        }
