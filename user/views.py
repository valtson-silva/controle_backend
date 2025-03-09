from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer

class UserRegisterView(APIView):
    # Registra um usuário no banco de dados
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                
                return Response({"success": "funciona"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "deu ruim"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Deu ruim"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):
    # Realiza o login do usuário
    
    def post(self, request):
        password = request.POST["password"]
        email = request.POST["email"]
        
        user = authenticate(
            request,
            email = email,
            password = password
        )
        
        if user is not None:
            login(request, user)
            
            return Response({"success": "funciona"}, status=status.HTTP_200_OK,)
        else:
            return Response({"error": "Usuário não é válido"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    # Realiza o logout do usuário
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        logout(request)
        request.session.flush()
        
        return Response({"success": "funciona"}, status=status.HTTP_200_OK)
