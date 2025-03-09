from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ExhaustsSerializer, ExhaustsCarModelSerializer
from .models import Exhausts, ExhaustsCarModel
from django.core.cache import cache
import json

class ExhaustCreateView(APIView):
    # Registra um escapamento no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ExhaustsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("exhaust_list")
            exhausts = Exhausts.objects.all()
            cache_serializer = ExhaustsSerializer(exhausts, many=True)
            cache.set("exhaust_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        

class ExhaustListView(APIView):
    # Mostra todos os escapamentos
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cache_list = cache.get("exhaust_list")
        
        if not cache_list:
            exhausts = Exhausts.objects.all()
            serializer = ExhaustsSerializer(exhausts, many=True)
            cache.set("exhaust_list", json.dumps(serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(json.loads(cache_list), status=status.HTTP_200_OK)
    
 
class ExhaustDetailView(APIView):
    # Mostra os detalhes de um escapemnto

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        cache_list = cache.get("exhaust_list")
        
        if not cache_list:
            try:
                exhausts = Exhausts.objects.get(id=id)
                serializer = ExhaustsSerializer(exhausts)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Não existe um escapamento com esse ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            exhaust = None
            for e in json.loads(cache_list):
                if e["id"] == id:
                    exhaust = e
                    
            if exhaust == None:
                return Response({"error": "Não existe um escapamento relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(exhaust, status=status.HTTP_200_OK)
            

class ExhaustQueryMarkListView(APIView):
    # Mostra todos escapamentos de uma marca
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, exhaust_mark_id):
        cache_list = cache.get("exhaust_list")
        
        if not cache_list:
            exhausts = Exhausts.objects.filter(exhaust_mark=exhaust_mark_id)
            serializer = ExhaustsSerializer(exhausts, many=True)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            exhausts = []
            for e in json.loads(cache_list):
                if e["exhaust_mark"] == exhaust_mark_id:
                    exhausts.append(e)
            
            return Response(exhausts, status=status.HTTP_200_OK)
    
    
class ExhaustUpdateView(APIView):
    # Atualiza os detalhes de um escapamento
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            exhaust = Exhausts.objects.get(id=id)
            serializer = ExhaustsSerializer(exhaust, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                cache.delete("exhaust_list")
                exhausts = Exhausts.objects.all()
                cache_serializer = ExhaustsSerializer(exhausts, many=True)
                cache.set("exhaust_list", json.dumps(cache_serializer.data), timeout=60*300)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe escapamento relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)


class ExhaustDeleteView(APIView):
    # Deleta um escapamento do banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            exhaust = Exhausts.objects.get(id=id)
            exhaust.delete()
            
            cache.delete("exhaust_list")
            exhausts = Exhausts.objects.all()
            cache_serializer = ExhaustsSerializer(exhausts, many=True)
            cache.set("exhaust_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            cache.delete("exhausts_car_model_list")
            exhaustsCarModel = ExhaustsCarModel.objects.all()
            cache_serializer = ExhaustsCarModelSerializer(exhaustsCarModel, many=True)
            cache.set("exhausts_car_model_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response({"success": "Escapamento deletado com sucesso"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe escapamento relacionado com esse ID"})
    