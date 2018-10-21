from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

from poemese.models import Poema
from poemese.forms import PostForm


# CRUD OF POEMS

@login_required(login_url='poemese:sign_in')
def read_poema(request):
    """ Read the first six poems by order of publication. """
    poema = Poema.objects.all().order_by('-dataPublicacao')[:6]
    # Return the poems to be rendered in posts.html
    return render(request, 'poemese/posts.html', {'object_list': poema})


def create_poema(request):
    """ Create a poem based in the poems' author and date of publication. """
    formulario_poema = PostForm(request.POST or None)
    # If request.method is equals to Post, then the user wants to submit the
    # poem.
    if request.method == 'POST':
        if formulario_poema.is_valid():
            poema = formulario_poema.save(commit=False)
            poema.autor_poema = request.user
            poema.dataPublicacao = datetime.datetime.now()
            poema.save()
            return redirect('poemese:poemas')
    return render(request, 'poemese/posts.html',
                  {'formulario_poema': formulario_poema})


def update_poema(request, pk):
    """ Update a poem based in a id

    Keyword arguments:
    pk -- id of a poem.
    """
    title = "Editar Poema"
    poema = get_object_or_404(Poema, pk=pk)
    formulario_atualizar_poema = PostForm(request.POST, instance=poema)
    # If request.method is equals to Post, then the user already edited the
    # poem and is submitting it, else, the user is requesting a new form to
    # edit the poem.
    if request.method == 'POST':
        if formulario_atualizar_poema.is_valid():
            formulario_atualizar_poema.save()
            return redirect('poemese:poemas')
    else:
        formulario_atualizar_poema = PostForm(instance=poema)
    return render(request, 'poemese/posts.html',
                  {'formulario_atualizar_poema': formulario_atualizar_poema,
                   'title': title})


def delete_poema(request, pk):
    """ Delete a poem based in a id

    Keyword arguments:
    pk -- id of a poem.
    """
    poema = get_object_or_404(Poema, pk=pk)
    if request.method == 'GET':
        poema.delete()
        return redirect('poemese:poemas')
    return render(request, 'poemese/posts.html', {'object': poema})


# LIST AND LOAD POEMS

def poemList(request, name):
    """ Load the first six user's poems """
    poema = Poema.objects.filter(autor_poema=name).order_by('-dataPublicacao')[:6]
    return render(request, 'poemese/posts.html', {'object_list': poema})


def loadMorePoems(request):
    """ Load poems on demand """
    name = request.GET.get('name', '')
    offset = request.GET['offset']
    if name != "": # Author's poems
        poemas = Poema.objects.filter(autor_poema=name).order_by('-dataPublicacao')[int(offset):(int(offset) + 6)]
    else: # Poetryline's poems
        poemas = Poema.objects.all().order_by('-dataPublicacao')[int(offset):(int(offset) + 6)]

    return render(request, 'poemese/loadpoems.html', {'poemas':poemas})
