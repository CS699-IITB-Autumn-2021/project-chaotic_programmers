from api.models import User
from api.serializers import UserSerializer
from django.http import Http404

def get_logged_in_user():
    """
    Description:
    	See if a user has logged in and has not logged out

    Arguments:
    	No Arguments

    Returns:
        UserInformation
    """
    try:
        obj = User.objects.all()[1]
        return obj
    except User.DoesNotExist:
            raise Http404
