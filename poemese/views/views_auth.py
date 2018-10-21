from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from poemese.forms import UserCreationForm, LoginForm


def sign_in(request):
    """ Sign in a user based in a pseudonym and a password """
    if request.method == 'POST':
        form = LoginForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.pseudonimo = request.POST['pseudonimo']
            form.password = request.POST['password']
            user = authenticate(username=form.pseudonimo, password=form.password)
            if user is not None:
                login(request, user)
                return redirect('poemese:poemas')

    return render(request, 'poemese/login.html', {
        'entry_form': LoginForm()
    })


def sign_up(request):
    """ Sign up a user """
    if request.method == 'POST':
        # Receive a form with the files and information needed to create a user
        form = UserCreationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Você foi cadastrado com sucesso!')
            return redirect('poemese:sign_in')
    return render(request, 'poemese/cadastro.html', {
        'register_form': UserCreationForm()
    })


def sign_out(request):
    """ Sign out the user """
    logout(request)
    return redirect("poemese:sign_in")
