from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from . serializers import UserSerializer


class SignUp(APIView):
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = UserSerializer(data=data)
        return Response(serializer.data)
                
        ...
    ...

# TODO: LogIn, Account, maybe an userlist
