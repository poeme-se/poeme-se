from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from poemese.forms import UserCreationForm, UserChangeForm
from poemese.models import Usuario, Poema, Livro, AprovacoesPoema, Comentario, \
                           AprovacoesComentario, Denuncia, Aparencia, RelacoesAmizade, \
                           Grupo, ParticipacaoGrupo, sugestao

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('pseudonimo','email', 'data_nascimento','nome_completo', 'is_admin', 'profile_image')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('pseudonimo', 'password')}),
        ('Personal info', {'fields': ('data_nascimento', 'nome_completo', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('profile_image', 'pseudonimo','email','nome_completo', 'data_nascimento', 'password1', 'password2')}
        ),
    )
    search_fields = ('pseudonimo',)
    ordering = ('pseudonimo',)
    filter_horizontal = ()

# modelo padrão não registrado
admin.site.unregister(Group)
# ações usuário
admin.site.register(Usuario, UserAdmin)
admin.site.register(Poema)
admin.site.register(AprovacoesPoema)
# obras
admin.site.register(Livro)
# relações usuário
admin.site.register(RelacoesAmizade)
admin.site.register(ParticipacaoGrupo)
admin.site.register(Comentario)
admin.site.register(AprovacoesComentario)
admin.site.register(Grupo)
admin.site.register(Denuncia)
# estilos
admin.site.register(Aparencia)
# Sugestões
admin.site.register(sugestao)
