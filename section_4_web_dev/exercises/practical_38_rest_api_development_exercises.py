"""
Упражнения к практической работе 38: Разработка REST API

Выполните упражнения по созданию REST API.
"""

# Упражнение 1: Flask REST API
def exercise_flask_rest():
    """
    Создайте REST API на Flask.
    """
    from flask import Flask, jsonify, request
    from flask_restful import Api, Resource
    
    app = Flask(__name__)
    api = Api(app)
    
    items = []
    
    class ItemList(Resource):
        def get(self):
            return {'items': items}
        
        def post(self):
            data = request.get_json()
            items.append(data)
            return {'item': data}, 201
    
    class Item(Resource):
        def get(self, item_id):
            if item_id < len(items):
                return {'item': items[item_id]}
            return {'error': 'Not found'}, 404
    
    api.add_resource(ItemList, '/items')
    api.add_resource(Item, '/items/<int:item_id>')
    
    app.run(debug=True)


# Упражнение 2: Django REST Framework
def exercise_drf():
    """
    Настройте Django REST Framework.
    """
    # serializers.py
    from rest_framework import serializers
    from .models import Product
    
    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ['id', 'name', 'price']
    
    # views.py
    from rest_framework import viewsets
    
    class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
    
    # urls.py
    from rest_framework.routers import DefaultRouter
    router = DefaultRouter()
    router.register(r'products', ProductViewSet)


# Упражнение 3: Аутентификация в API
def exercise_api_auth():
    """
    Добавьте аутентификацию в API.
    """
    from rest_framework.authentication import TokenAuthentication
    from rest_framework.permissions import IsAuthenticated
    
    # views.py
    from rest_framework.views import APIView
    from rest_framework.response import Response
    
    class ProtectedView(APIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        
        def get(self, request):
            return Response({'user': request.user.username})


if __name__ == "__main__":
    print("Упражнения по REST API")
