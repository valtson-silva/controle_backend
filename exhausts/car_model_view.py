from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CarModelSerializer
from .models import CarModel
from django.core.cache import cache
import json

class CarModelCreateView(APIView):
    # Registra um modelo de carro no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CarModelSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("car_model_list")
            carModel = CarModel.objects.all()
            cache_serializer = CarModelSerializer(carModel, many=True)
            cache.set("car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        

class CarModelListView(APIView):
    # Mostra todos os modelos de carros
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cache_list = cache.get("car_model_list")
        
        if not cache_list:
            carMordels = CarModel.objects.all()
            serializer = CarModelSerializer(carMordels, many=True)
            cache.set("car_model_list", json.dumps(serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(json.loads(cache_list), status=status.HTTP_200_OK)
        
class CarModelDetailView(APIView):
    # Mostra os detalhes de um modelo de carro
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        cache_list = cache.get("car_model_list")
        
        if not cache_list:
            try:
                carModel = CarModel.objects.get(id=id)
                serializer = CarModelSerializer(carModel)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Não existe um modelo de carro com esse ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            carModel = None
            for cm in json.loads(cache_list):
                if cm["id"] == id:
                    carModel = cm
                    
            if carModel == None:
                return Response({"error": "Não existe um modelo de carro relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(carModel, status=status.HTTP_200_OK)


class CarModelUpdateView(APIView):
    # Atualiza os detalhes de um modelo de carro
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            carModel = CarModel.objects.get(id=id)
            serializer = CarModelSerializer(carModel, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                cache.delete("car_model_list")
                carModels = CarModel.objects.all()
                cache_serializer = CarModelSerializer(carModels, many=True)
                cache.set("car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe modelo de carro relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
            
            
class CarModelDeleteView(APIView):
    # Deleta um modelo de carro do banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            carModel = CarModel.objects.get(id=id)
            carModel.delete()
            
            cache.delete("car_model_list")
            carModels = CarModel.objects.all()
            cache_serializer = CarModelSerializer(carModels, many=True)
            cache.set("car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response({"success": "Modelo de carro deletada com sucesso"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe modelo de carro relacionado com esse ID"})
        