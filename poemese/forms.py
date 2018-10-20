from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from poemese.models import Usuario, Poema, Livro
from poemese.choices import *
from material import *

class UserCreationForm(forms.ModelForm):

    profile_image = forms.ImageField(label="Imagem")
    pseudonimo = forms.CharField(label='Pseudônimo')
    nome_completo = forms.CharField(label='Nome Completo')
    email = forms.EmailField(label='E-mail')
    data_nascimento = forms.DateField(label='Data Nascimento')

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('profile_image', 'pseudonimo', 'nome_completo', 'data_nascimento', 'email')
        widgets = {

        }

    layout = Layout(
        Row('profile_image'),
        Row('pseudonimo', 'nome_completo'),
        Row('email','data_nascimento'),
        Row('password1', 'password2')
    )


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas não coincidem")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField()
    class Meta:
        model = Usuario
        fields = ('nome_completo','email',
                  'data_nascimento')

    def clean_password(self):
        return self.initial["password"]

class PostForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.Textarea, label="Título")
    conteudo = forms.CharField(widget=forms.Textarea, label="Conteúdo")
    class Meta:
        model = Poema
        fields = ('titulo', 'conteudo')


class LoginForm(forms.Form):
    pseudonimo = forms.CharField(label='Pseudônimo')
    password = forms.CharField(widget=forms.PasswordInput)
    keep_logged = forms.BooleanField(required=False, label="Mantenha-me conectado")

class BookForm(forms.ModelForm):
    titulo_book = forms.CharField(label='Título')
    dataPublicacao = forms.DateField(label="Data de Publicação")
    nome_autor = forms.CharField(label='Nome do autor')
    resumo = forms.CharField(widget=forms.Textarea, label='Resumo')
    avaliacao = forms.IntegerField(widget=forms.Select(choices=AVALIATION_CHOICES), initial='', required=True, label='Avaliação')
    capa_livro = forms.ImageField(label='Imagem')

    class Meta:
        model = Livro
        fields = ('titulo_book', 'dataPublicacao', 'nome_autor', 'resumo', 'avaliacao', 'capa_livro')

    layout = Layout(
        Row('titulo_book', 'dataPublicacao', 'avaliacao'),
        Row('resumo'),
        Row('nome_autor','capa_livro')
    )
    


class UploadForm_Image(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('profile_image',)
