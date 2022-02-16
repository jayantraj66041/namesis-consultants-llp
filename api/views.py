from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from api.models import User
from .serializers import SignUpSerializer, LogInSerializer, UserSerializer

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class LogInView(TokenViewBase):
    serializer_class = LogInSerializer

class Dashboard(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        me = User.objects.get(username=request.user)
        users = User.objects.all().exclude(username=request.user)
        serializer = UserSerializer(users, many=True)
        return Response({
            'fname': me.first_name,
            'lname': me.last_name,
            'email': me.email,
            'username': me.username,
            'address': me.address,
            'users': serializer.data
        })
    

class Action(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        if User.objects.get(username=request.user).pk != id:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': "Invalid Id"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        if User.objects.get(username=request.user).pk != id:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid Id"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if User.objects.get(username=request.user).pk != id:
            user = User.objects.get(pk=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid Id"}, status=status.HTTP_400_BAD_REQUEST)