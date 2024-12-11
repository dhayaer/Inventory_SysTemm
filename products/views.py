from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Variant, SubVariant
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import JsonResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json



# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    class Meta:
        model = Product
        fields = ['product_id', 'product_code', 'product_name', 'product_image', 'total_stock', 'name', 'price']

# Variant Serializer
class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'product']

# SubVariant Serializer
class SubVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariant
        fields = ['id', 'option', 'variant', 'stock']

# Create Product API
@api_view(['POST'])
@csrf_exempt  # Remove in production and use proper authentication
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsing the JSON request body
            product_name = data.get('name')
            product_price = data.get('price')
            
            # Check for missing data
            if not product_name or not product_price:
                return JsonResponse({'error': 'Missing product name or price'}, status=400)
            
            # Creating the product
            product = Product.objects.create(name=product_name, price=product_price)
            
            # Respond with a success message and product details
            return JsonResponse({'message': 'Product created successfully', 'product_id': product.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed. Use POST.'}, status=405)

# List Products API
@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Add Stock API
@api_view(['POST'])
def add_stock(request):
    if request.method == 'POST':
        data = request.data
    try:
        subvariant = SubVariant.objects.get(id=data['sub_variant_id'])
        subvariant.stock += data['quantity']
        subvariant.save()

        return Response({"message": "Stock added successfully!"}, status=status.HTTP_200_OK)
    except SubVariant.DoesNotExist:
        return Response({"error": "SubVariant not found"}, status=status.HTTP_400_BAD_REQUEST)

# Remove Stock API
@api_view(['POST'])
def remove_stock(request):
    if request.method == 'POST':
        data = request.data
    try:
        subvariant = SubVariant.objects.get(id=data['sub_variant_id'])
        if subvariant.stock >= data['quantity']:
            subvariant.stock -= data['quantity']
            subvariant.save()

            return Response({"message": "Stock removed successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)

    except SubVariant.DoesNotExist:
        return Response({"error": "SubVariant not found"}, status=status.HTTP_400_BAD_REQUEST)
def remove_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)