from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Crop, CropMaster

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

# ✅ Crop Recommendation API (already written)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def crop_recommendation(request):
    try:
        # Step 1: Extract and validate input data
        data = request.data
        soil_texture = data.get('soil_texture')
        organic_matter = data.get('organic_matter')
        drainage_status = data.get('drainage_status')

        try:
            soil_ph = float(data.get('soil_ph', 0))
            rainfall_mm = float(data.get('rainfall_mm', 0))
            avg_temperature = float(data.get('avg_temperature', 0))
        except ValueError:
            return Response({"error": "Soil pH, rainfall, and temperature must be valid numbers."}, status=status.HTTP_400_BAD_REQUEST)

        if not all([soil_texture, organic_matter, drainage_status]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Save user input
        Crop.objects.create(
            user=request.user,  # Optional: only if linked to User
            soil_texture=soil_texture,
            soil_ph=soil_ph,
            organic_matter=organic_matter,
            drainage_status=drainage_status,
            rainfall_mm=rainfall_mm,
            avg_temperature=avg_temperature
        )

        # Step 3: Recommendation logic
        matching_crops = CropMaster.objects.filter(
            soil_texture=soil_texture,
            organic_matter=organic_matter,
            drainage=drainage_status,
            ph_min__lte=soil_ph,
            ph_max__gte=soil_ph,
            rainfall_min__lte=rainfall_mm,
            rainfall_max__gte=rainfall_mm,
            temperature_min__lte=avg_temperature,
            temperature_max__gte=avg_temperature
        )

        recommendations = [crop.name for crop in matching_crops]

        # Step 4: Return response
        return Response({'recommended': recommendations}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
