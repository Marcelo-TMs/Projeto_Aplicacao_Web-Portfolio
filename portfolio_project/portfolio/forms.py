from django import forms
from django.contrib.auth.models import User
from .models import Projeto, Perfil

# Formulário para o modelo Projeto
class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = [
            'titulo',
            'descricao',
            'imagem',
            'link'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do projeto'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Descreva o projeto...'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cole aqui o link para o projeto (opcional)'
            }),
        }

# Formulário para o modelo Perfil
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'bio',
            'habilidades',
            'linkedin',
            'github',
            'imagem_perfil'
        ]

        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Escreva uma breve descrição sobre você'
            }),
            'habilidades': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Liste suas principais habilidades (exemplo: Python, Django, HTML...)'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cole aqui o link do seu LinkedIn (opcional)'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cole aqui o link do seu GitHub (opcional)'
            }),
        }
        labels = {
            'imagem_perfil': 'Foto de Perfil',
            'bio': 'Biografia',
            'habilidades': 'Habilidades',
            'linkedin': 'LinkedIn',
            'github': 'GitHub',
        }

# Formulário para mudar o nome do User
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu nome de usuário'
            })
        }
        labels = {
            'username': 'Nome de Usuário',
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        # Verifica se já existe outro usuário com esse nome
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esse nome de usuário já está em uso. Escolha outro.")

        return username
