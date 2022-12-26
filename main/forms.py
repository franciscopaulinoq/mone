from django import forms
from main.models import *

# Create your forms here.

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields= '__all__'

        labels = {
            'nome' : '',
            'tipo' : '',
            'cor' : '',
        }
        widgets = {
            'nome' : forms.TextInput(attrs={'class' : 'form-control form-control-user', 'type' : 'text', 'placeholder' : 'Nome', 'required' : 'true'}),
            'tipo' : forms.RadioSelect(attrs={'class' : '', 'type' : 'radio', 'required' : 'true'}),
            'cor' : forms.TextInput(attrs={'class' : 'form-control form-control-user', 'type' : 'text', 'placeholder' : '#000000', 'required' : 'true'}),
        }

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields= '__all__'

        labels = {
            'descricao' : '',
            'valor' : '',
            'data' : '',
            'categoria' : '',
        }
        widgets = {
            'descricao' : forms.TextInput(attrs={'class' : 'form-control form-control-user', 'type' : 'text', 'placeholder' : 'Descrição', 'required' : 'true'}),
            'valor' : forms.NumberInput(attrs={'class' : 'form-control form-control-user', 'type' : 'number', 'placeholder' : 'Valor', 'min' : '0', 'step' : '0.01','required' : 'true'}),
            'data' : forms.DateInput(format=('%Y-%m-%d'), attrs={'class' : 'form-control form-control-user', 'type' : 'date', 'required' : 'true'}),
            'categoria' : forms.Select(attrs={'class' : 'form-control form-control-user', 'required' : 'true'}),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields= '__all__'

        labels = {
            'descricao' : '',
            'valor' : '',
            'data' : '',
            'categoria' : '',
        }
        widgets = {
            'descricao' : forms.TextInput(attrs={'class' : 'form-control form-control-user', 'type' : 'text', 'placeholder' : 'Descrição', 'required' : 'true'}),
            'valor' : forms.NumberInput(attrs={'class' : 'form-control form-control-user', 'type' : 'number', 'placeholder' : 'Valor', 'min' : '0', 'step' : '0.01','required' : 'true'}),
            'data' : forms.DateInput(format=('%Y-%m-%d'),attrs={'class' : 'form-control form-control-user', 'type' : 'date', 'required' : 'true'}),
            'categoria' : forms.Select(attrs={'class' : 'form-control form-control-user', 'required' : 'true'}),
        }