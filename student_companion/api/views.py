from api.models import TestModel
from api.serializers import TestModelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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