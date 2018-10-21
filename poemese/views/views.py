from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse

from poemese.models import Poema, Usuario, Livro, RelacoesAmizade, Grupo, AprovacoesPoema, Comentario, sugestao
from poemese.forms import UserCreationForm, UserChangeForm, PostForm, LoginForm, UploadForm_Image, BookForm



# list of groups
def groupList(request):
    group = Grupo.objects.all()[:4]
    data = {}
    data['object_list'] = group
    return render(request, 'poemese/groups.html', data)


# list of follow
def followList(request, name):
    user = Usuario.objects.get(pk=name)
    followers = RelacoesAmizade.objects.filter(destino=user)[:6] # Relations with follower on the 'origem'
    following = RelacoesAmizade.objects.filter(origem=user)[:6] # Relations with target of following on the 'destino'
    return render(request, 'poemese/friendlist.html', { 'followers':followers, 'following':following })

# Search friends
def search_friends_view(request):
    user_name = request.GET.get('friend_name', False)
    # Followers with this name
    followers = RelacoesAmizade.objects.filter(origem__pseudonimo__icontains=user_name, destino=request.user)[:6]
    # Followings with this name
    following = RelacoesAmizade.objects.filter(origem=request.user, destino__pseudonimo__icontains=user_name)[:6]
    return render(request, 'poemese/loadFriends.html', { 'followers':followers, 'following':following })


# List of the books
def bookList(request):
    livros=""
    if request.method == 'GET':
        livros = Livro.objects.all()[:6]
        book_form = BookForm()

    if request.method == 'POST':
        book_form = BookForm(request.POST or None, request.FILES or None)
        if book_form.is_valid():
            book_form.save()
            messages.success(request, 'Livro cadastrado com sucesso!')
            return redirect('poemese:bookList')

    return render(request, 'poemese/obras.html', {'book_form':book_form, 'object_list':livros})

# Search books
def search_works_view(request):
    title = request.GET.get('title', False)
    obras = Livro.objects.filter(titulo_book__icontains=title)[:8] # It's necessary to filter dinamically by pieces of words
    result = list(obras.values())
    data={}
    data['object_list'] = result
    return render(request, 'poemese/loadWorks.html', data)

# Add likes
def addLike(request):
    date = request.GET['date']
    pseudonimo = Usuario.objects.get(pk=request.GET.get('name', None))
    id_poem = Poema.objects.get(pk=request.GET.get('id_poem', None))
    likes = AprovacoesPoema.objects.filter(aprovador=pseudonimo, id_poema=id_poem)
    if len(likes) == 1:
      likes.delete()
    elif len(likes) == 0:
      AprovacoesPoema.objects.create(aprovador=pseudonimo, id_poema=id_poem, data=date)
    data = {
        "number" : len(AprovacoesPoema.objects.filter(id_poema=id_poem))
    }
    Poema.objects.filter(pk=request.GET.get('id_poem', None)).update(qtd_gostei=data['number'])
    return JsonResponse(data)

def follow_friend_view(request):
    followed_user = Usuario.objects.get(pk=request.GET.get('id_followed', None))
    follower_user = Usuario.objects.get(pk=request.GET.get('id_follower', None))
    date = request.GET['date']
    test_if_follow = RelacoesAmizade.objects.filter(origem=follower_user, destino=followed_user)

    if (test_if_follow.count() == 1):
        test_if_follow.delete()
    else:
        RelacoesAmizade.objects.create(origem=follower_user, destino=followed_user, data=date)

    data = {
        "if_follow" : RelacoesAmizade.objects.filter(origem=follower_user, destino=followed_user).count()
    }
    return JsonResponse(data)

# Views de sugestões

def addSuggestion(request):
    author_suggestion = Usuario.objects.get(pk=request.GET.get('name', None))
    id_poem = Poema.objects.get(pk=request.GET.get('id_poem', None))
    content = request.GET['content']
    date = request.GET['date']
    rate = request.GET['poem_rate']
    sugestao.objects.create(id_autor=author_suggestion, id_poema=id_poem, conteudo=content, dataPublicacao=date, valor_aprovacao=rate)
    return HttpResponse('')

def loadSuggestions(request):
    id_poem = Poema.objects.get(pk=request.GET.get('id_poem', None))
    suggestions = sugestao.objects.filter(id_poema=id_poem).order_by("pk")
    return render(request, 'poemese/loadSuggestions.html', {'suggestions':suggestions})

# Views de comentário
def loadComments(request):
    id_poem = Poema.objects.get(pk=request.GET.get('id_poem', None))
    comments = Comentario.objects.filter(id_poema=id_poem).order_by("pk")
    return render(request, 'poemese/loadComments.html', {'comments':comments})

def addComment(request):
    pseudonimo = Usuario.objects.get(pk=request.GET.get('name', None))
    id_poem = Poema.objects.get(pk=request.GET.get('id_poem', None))
    content = request.GET['content']
    date = request.GET['date']
    Comentario.objects.create(id_autor=pseudonimo, id_poema=id_poem, conteudo=content, dataPublicacao=date)
    return HttpResponse('')

# Editar informações dos usuários
def config(request):
    user_profile = Usuario.objects.get(pk=request.user)
    if request.method == 'POST':
        formEdit = UserChangeForm(request.POST, instance=user_profile, prefix='edit_form')
        img = UploadForm_Image(request.POST or None, request.FILES or None, instance=user_profile, prefix='img_form')
        if formEdit.is_valid():
            formEdit.save()
            return redirect('/settings/')
        else:
            print(formEdit.errors)
        if img.is_valid():
            profile = img.save(commit=False)
            profile.save()
            return redirect('/settings/')
        else:
            print(img.errors)

    extra_context = {
        'formEdit': UserChangeForm(instance=user_profile, prefix='edit_form'),
        'update_image_form': UploadForm_Image(prefix='img_form'),
        'user': user_profile
    }
    return render(request, 'poemese/config.html', extra_context)
