from api.models import User
from api.serializers import UserSerializer
from django.http import Http404

def get_logged_in_user():
    try:
        obj = User.objects.all()[1]
        return obj
    except User.DoesNotExist:
            raise Http404
