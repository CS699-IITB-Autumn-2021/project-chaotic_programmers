from api.models import FlashDeck, TestModel, User, UserRelation
from api.serializers import FlashDeckSerializer, TestModelSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.lib import get_logged_in_user


class TestModelList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        objects  = TestModel.objects.all()
        serializer = TestModelSerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestModelDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return TestModel.objects.get(pk=pk)
        except TestModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = TestModelSerializer(obj)
        return Response(serializer.data)

class DeckModelList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        objects  = FlashDeck.objects.all()
        serializer = FlashDeckSerializer(objects, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = TestModelSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoggedinUserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, format=None):
        resp = get_logged_in_user()
        serializer = UserSerializer(resp)
        return Response(serializer.data)


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, key, value):
        #Getting user object which has correct value for that key
        kwargs = {
            '{0}'.format(key) : '{0}'.format(value)
        }
        try:
            current_user_id = get_logged_in_user().id
            queryset = User.objects.all().exclude(id = current_user_id)
            result =  queryset.filter(**kwargs)
            if(len(result) == 0):
                raise Http404
            return result[0]
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        search_key = request.query_params.get('key')
        search_value = request.query_params.get('value')
        obj = self.get_object(search_key, search_value)
        serializer = UserSerializer(obj)
        return Response(serializer.data)


class FriendDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def post(self, request, format=None):
        print("\n\n\n\n\n")
        print(request.data)
        friend_user_id = request.data['friend_id']
        if not friend_user_id:
            raise Http404
        current_user = get_logged_in_user()
        new_user = User.objects.get(id = friend_user_id)
        current_user.relations.add(new_user)
        current_user.save()
        serializer = UserSerializer(current_user)
        return Response(serializer.data)

class FriendList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        current_user = get_logged_in_user()
        objects  = current_user.relations.all()
        serializer = UserSerializer(objects, many=True)
        return Response(serializer.data)