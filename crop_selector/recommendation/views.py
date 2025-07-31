# crop_selector/recommendation/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Crop, CropMaster
from .serializers import CropSerializer


# ✅ Register API
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)

    return Response({'token': token.key, 'username': user.username}, status=status.HTTP_201_CREATED)


# ✅ Login API
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ Logout API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


# ✅ Crop Recommendation API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def crop_recommendation(request):
    try:
        data = request.data
        print("📥 Incoming data:", data)

        # Validate and extract numeric values
        try:
            soil_ph = float(data.get("soil_ph", 0))
            rainfall = float(data.get("rainfall_mm", 0))
            temperature = float(data.get("avg_temperature", 0))
        except (ValueError, TypeError):
            return Response({"error": "Invalid numeric input values."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract and clean categorical inputs
        soil_texture = data.get("soil_texture", "").strip()
        organic_matter = data.get("organic_matter", "").strip()
        drainage_status = data.get("drainage_status", "").strip()

        # Validate presence
        if not (soil_texture and organic_matter and drainage_status):
            return Response({"error": "Missing required field(s)."}, status=status.HTTP_400_BAD_REQUEST)

        # Query CropMaster with relaxed matching
        crops = CropMaster.objects.filter(
    Q(soil_texture__icontains=soil_texture) | Q(soil_texture__iexact=soil_texture),
    Q(drainage__icontains=drainage_status) | Q(drainage__iexact=drainage_status),
    organic_matter__iexact=organic_matter,
    ph_min__lte=soil_ph,
    ph_max__gte=soil_ph,
    rainfall_min__lte=rainfall,
    rainfall_max__gte=rainfall,
    temperature_min__lte=temperature,
    temperature_max__gte=temperature,
)
        print("🔍 Filtered crops:", crops)
        if not crops.exists():
            return Response({"message": "No suitable crops found for the given input."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CropSerializer(crops, many=True)
        print("✅ Recommendations:", serializer.data)

        if serializer.data:
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No suitable crops found for the given input."}, status=200)

    except Exception as e:
        print("🔥 Unexpected error:", str(e))
        return Response({"error": "Internal server error."}, status=500)
