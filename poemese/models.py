from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
from poemese.choices import *

class UsuarioManager(BaseUserManager):
    def create_user(self, pseudonimo, password, email, nome_completo, data_nascimento):
        user = self.model(pseudonimo=pseudonimo,
                          email=self.normalize_email(email),
                          nome_completo=nome_completo,
                          data_nascimento=data_nascimento)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, pseudonimo, password, email, nome_completo, data_nascimento):
        user = self.create_user(
            pseudonimo=pseudonimo,
            password=password,
            email=email,
            nome_completo=nome_completo,
            data_nascimento=data_nascimento
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    profile_image = models.ImageField(upload_to='media/profile-images/', null=True, blank=True)
    pseudonimo = models.CharField(max_length=20, primary_key=True)
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    number_of_likes = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'pseudonimo'
    REQUIRED_FIELDS = ['email','nome_completo','data_nascimento']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def get_full_name(self):
        return self.nome_completo

    def get_short_name(self):
        return self.pseudonimo

    def __str__(self):
        return self.pseudonimo

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Poema(models.Model):
    autor_poema = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    titulo = models.TextField()
    conteudo = models.TextField()
    dataPublicacao = models.DateField(default='1999-11-11')
    qtd_gostei = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'poema'
        verbose_name_plural = 'poemas'

    def __str__(self):
        return self.titulo

class AprovacoesPoema(models.Model):
    aprovador = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_poema = models.ForeignKey('poemese.Poema', on_delete=models.DO_NOTHING)
    data = models.DateField(default='1999-11-11')

class Livro(models.Model):
    titulo_book = models.CharField(max_length=150)
    dataPublicacao = models.DateField(default='1999-11-11')
    nome_autor = models.CharField(max_length=150)
    resumo = models.CharField(max_length=1000, default='')
    avaliacao = models.IntegerField(choices=AVALIATION_CHOICES, default=1)
    capa_livro = models.ImageField(upload_to='media/book-cover/', null=True, blank=True)

    class Meta:
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.titulo_book

class Comentario(models.Model):
    id_autor = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_poema = models.ForeignKey('poemese.Poema', on_delete=models.DO_NOTHING)
    conteudo = models.TextField()
    dataPublicacao = models.DateField(default='1999-11-11')
    qtd_gostei = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __str__(self):
        return self.conteudo

class sugestao(models.Model):
    id_autor = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_poema = models.ForeignKey('poemese.Poema', on_delete=models.DO_NOTHING)
    conteudo = models.TextField()
    dataPublicacao = models.DateField(default='1999-11-11')
    valor_aprovacao = models.DecimalField(max_digits=2, decimal_places=1)

class AprovacoesComentario(models.Model):
    aprovador = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_comentario = models.ForeignKey('poemese.Comentario', on_delete=models.DO_NOTHING)
    data = models.DateField(default='1999-11-11')

class Denuncia(models.Model):
    id_autor = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_poema = models.ForeignKey('poemese.Poema', on_delete=models.DO_NOTHING)
    conteudo = models.TextField()
    dataPublicacao = models.DateField(default='1999-11-11')
    is_valid = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'denuncia'
        verbose_name_plural = 'denuncias'

    def __str__(self):
        return self.conteudo

class Aparencia(models.Model):
    id_autor = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    cores = models.CharField(max_length=128)
    fonte = models.CharField(max_length=128)
    ''' O atributo cores será subdividido em vários, formando uma palheta de cores customizável '''
    class Meta:
        verbose_name = 'aparencia'
        verbose_name_plural = 'aparencia'

class RelacoesAmizade(models.Model):
    origem = models.ForeignKey('poemese.Usuario', related_name='origin_relations', on_delete=models.DO_NOTHING)
    destino = models.ForeignKey('poemese.Usuario', related_name='destiny_relations', on_delete=models.DO_NOTHING)
    data = models.DateField(default='1999-11-11')

class Grupo(models.Model):
    nome = models.CharField(max_length=128)
    categoria = models.CharField(max_length=128)
    membros = models.ManyToManyField('poemese.Usuario', through='ParticipacaoGrupo')

    def __str__(self):
        return self.nome

class ParticipacaoGrupo(models.Model):
    id_usuario = models.ForeignKey('poemese.Usuario', on_delete=models.DO_NOTHING)
    id_grupo = models.ForeignKey('poemese.Grupo', on_delete=models.DO_NOTHING)
    data_entrada = models.DateField(default='1999-11-11')
    status_aprovacao = models.BooleanField(default=False)
    administrador = models.BooleanField(default=False)
