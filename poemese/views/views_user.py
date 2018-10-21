from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from poemese.models import Poema, Usuario, RelacoesAmizade


@login_required(login_url="poemese:sign_in")
def profile(request, pseudonimo):
    profile_user = Usuario.objects.get(pk=pseudonimo)
    poemas = Poema.objects.filter(autor_poema=pseudonimo)

    # Update the likes in profile
    update_likes(profile_user, poemas)

    # Verify if the user that requested the profile is following the profile's user
    is_follower = is_following(request.user, profile_user)

    followers = RelacoesAmizade.objects.filter(destino=profile_user).count()
    following = RelacoesAmizade.objects.filter(origem=profile_user).count()

    return render(request, 'poemese/perfil.html',
                  {'profile_user': profile_user, 'following': following,
                   'followers': followers, 'is_follower': is_follower, 'poem_list': poemas})


def update_likes(user, poemas):
    """ Update the poems' number of likes of the profile that has been open """
    likes = 0
    for poema in poemas:
        likes += poema.qtd_gostei
    user.number_of_likes = likes
    user.save()


def is_following(request_user, profile_user):
    """ Return True in case the user that requested follow the profile's user """
    relationship = RelacoesAmizade.objects.filter(origem=request_user, destino=profile_user)
    if request_user != profile_user:
        if relationship is not None:
            return True
        return False
