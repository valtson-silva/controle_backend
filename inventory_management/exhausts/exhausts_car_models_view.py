from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ExhaustsCarModelSerializer, ExhaustsSerializer
from .models import ExhaustsCarModel, Exhausts
from django.core.cache import cache
import json

class ExhaustsCarModelCreateView(APIView):
    # Registra informações no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ExhaustsCarModelSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("exhausts_car_model_list")
            exhaustsCarModel = ExhaustsCarModel.objects.all()
            cache_serializer = ExhaustsCarModelSerializer(exhaustsCarModel, many=True)
            cache.set("exhausts_car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        

class ExhaustsCarModelListView(APIView):
    # Mostra todos os escapamentos de um modelo de carro
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, car_model_id):
        cache_list = cache.get("exhausts_car_model_list")
        
        if not cache_list:
            exhausts = Exhausts.objects.filter(exhaustscarmodel__car_model__id=car_model_id)
            serializer = ExhaustsSerializer(exhausts, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            exhausts = []
            for ecm in json.loads(cache_list):
                if ecm["car_model"] == car_model_id:
                    exhausts.append(ExhaustsSerializer(Exhausts.objects.get(id=ecm["exhaust"])).data)
                        
                        
            return Response(exhausts, status=status.HTTP_200_OK)
        
class ExhaustsCarListView(APIView):
    # Mostra todos os escapamentos e modelos de carros
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cache_list = cache.get("exhausts_car_model_list")
        
        if not cache_list:
            exhausts = ExhaustsCarModel.objects.all()
            serializer = ExhaustsSerializer(exhausts, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:           
            return Response(json.loads(cache_list), status=status.HTTP_200_OK)


class ExhaustsCarModelUpdateView(APIView):
    # Atualiza os detalhes de um registro
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            exhaustsCarModel = ExhaustsCarModel.objects.get(id=id)
            serializer = ExhaustsCarModelSerializer(exhaustsCarModel, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                cache.delete("exhausts_car_model_list")
                exhaustsCarModel = ExhaustsCarModel.objects.all()
                cache_serializer = ExhaustsCarModelSerializer(exhaustsCarModel, many=True)
                cache.set("exhausts_car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe registro relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
        