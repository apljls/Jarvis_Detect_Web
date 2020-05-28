from django import forms
from .models import Menu, DetectPeople, DetectFaces, DetectPeople_lcl, DeleteArquivoBucket, TipoColaborador


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'


class DetectPeopleForm(forms.ModelForm):
    class Meta:
        model = DetectPeople
        fields = '__all__'


class DetectFacesForm(forms.ModelForm):
    class Meta:
        model = DetectFaces
        fields = '__all__'


class DetectPeopleForm_lcl(forms.ModelForm):
    class Meta:
        model = DetectPeople_lcl
        fields = '__all__'


class DeleteArquivosForm(forms.ModelForm):
    class Meta:
        model = DeleteArquivoBucket
        fields = '__all__'


class TipoColaboradorForm(forms.ModelForm):
    class Meta:
        model = TipoColaborador
        fields = '__all__'
