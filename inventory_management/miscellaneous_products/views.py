from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MiscellaneousProductsSerializer
from .models import MiscellaneousProducts
from django.core.cache import cache
import json

class MiscellaneousProductsCreateView(APIView):
    # Registra um produto no banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = MiscellaneousProductsSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("miscellaneous_products_list")
            miscellaneousProducts = MiscellaneousProducts.objects.all()
            cache_serializer = MiscellaneousProductsSerializer(miscellaneousProducts, many=True)
            cache.set("miscellaneous_products_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        

class MiscellaneousProductsListView(APIView):
    # Mostra todos os produtos
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cache_list = cache.get("miscellaneous_products_list")
        
        if not cache_list:
            miscellaneousProducts = MiscellaneousProducts.objects.all()
            serializer = MiscellaneousProductsSerializer(miscellaneousProducts, many=True)
            
            cache.set("miscellaneous_products_list", json.dumps(serializer.data), timeout=60*300)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(json.loads(cache_list), status=status.HTTP_200_OK)
            

class MiscellaneousProductsDetailView(APIView):
    # Mostra as informções de um produto
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        cache_list = cache.get("miscellaneous_products_list")
        
        if not cache_list:
            try:
                miscellaneousProducts = MiscellaneousProducts.objects.get(id=id)
                serializer = MiscellaneousProductsSerializer(miscellaneousProducts)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({"error": "Não existe um produto relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            miscellaneousProducts = None
            for mp in json.loads(cache_list):
                if mp["id"] == id:
                    miscellaneousProducts = mp
                    
            if miscellaneousProducts == None:
                return Response({"error": "Não existe um produto relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(miscellaneousProducts, status=status.HTTP_200_OK)
            

class MiscellaneousProductsUpdateView(APIView):
    # Atualiza as informações de um produto
    
    permission_classes = [IsAuthenticated]
    
    def put(self, request, id):
        try:
            miscellaneousProducts = MiscellaneousProducts.objects.get(id=id)
            serializer = MiscellaneousProductsSerializer(miscellaneousProducts, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                cache.delete("miscellaneous_products_list")
                miscellaneousProducts = MiscellaneousProducts.objects.all()
                cache_serializer = MiscellaneousProductsSerializer(miscellaneousProducts, many=True)
                cache.set("miscellaneous_products_list", json.dumps(cache_serializer.data), timeout=60*300)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Não existe produto relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)


class MiscellaneousProductsDeleteView(APIView):
    # Deleta um produto do banco de dados
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        try:
            miscellaneousProducts = MiscellaneousProducts.objects.get(id=id)
            miscellaneousProducts.delete()
            
            cache.delete("miscellaneous_products_list")
            miscellaneousProducts = MiscellaneousProducts.objects.all()
            cache_serializer = MiscellaneousProductsSerializer(miscellaneousProducts, many=True)
            cache.set("miscellaneous_products_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            return Response({"success": "Produto deletado com sucesso"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Não existe produto relacionado com esse ID"}, status=status.HTTP_404_NOT_FOUND)
            