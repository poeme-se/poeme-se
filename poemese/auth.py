from poemese.models import Usuario

class PseudoLogin(object):

    def authenticate(self, pseudonimo=None, password=None):
        kwargs = {'pseudonimo': pseudonimo}

        try:
            user = Usuario.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist:
            return None

def get_user(self, pseudonimo):
    try:
        user = Usuario.objects.get(pk=pseudonimo)
    except Usuario.DoesNotExist:
        return None