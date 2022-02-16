from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import status
from .serializers import SignUpSerializer, LogInSerializer

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
    def get(self, request):
        pass

