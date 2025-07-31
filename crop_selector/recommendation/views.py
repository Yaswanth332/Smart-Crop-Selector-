# crop_selector/recommendation/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Crop, CropMaster
from .serializers import CropSerializer, CropMasterSerializer  # Fixed: Added CropMasterSerializer


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


# ✅ Fixed Crop Recommendation API
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

        print(f"🔍 Searching for crops with:")
        print(f"   - Soil Texture: {soil_texture}")
        print(f"   - Drainage: {drainage_status}")
        print(f"   - Organic Matter: {organic_matter}")
        print(f"   - pH: {soil_ph}")
        print(f"   - Rainfall: {rainfall}")
        print(f"   - Temperature: {temperature}")

        # Fixed: Query CropMaster with correct field names
        crops = CropMaster.objects.filter(
            Q(soil_texture__icontains=soil_texture) | Q(soil_texture__iexact=soil_texture),
            Q(drainage_status__icontains=drainage_status) | Q(drainage_status__iexact=drainage_status),  # Fixed: drainage -> drainage_status
            organic_matter__iexact=organic_matter,
            soil_ph_min__lte=soil_ph,  # Fixed: ph_min -> soil_ph_min
            soil_ph_max__gte=soil_ph,  # Fixed: ph_max -> soil_ph_max
            rainfall_min__lte=rainfall,
            rainfall_max__gte=rainfall,
            temperature_min__lte=temperature,
            temperature_max__gte=temperature,
        )
        
        print(f"🔍 Found {crops.count()} crops matching criteria")
        
        if not crops.exists():
            # Try a more lenient search if no exact matches
            print("🔄 Trying lenient search...")
            crops = CropMaster.objects.filter(
                Q(soil_texture__icontains=soil_texture.split()[0]) |  # Match first word of soil texture
                Q(organic_matter__iexact=organic_matter) |
                Q(drainage_status__icontains=drainage_status.split()[0])  # Match first word of drainage
            )
            
            if crops.exists():
                print(f"🔍 Lenient search found {crops.count()} crops")
            else:
                return Response({
                    "message": "No suitable crops found for the given input.",
                    "suggestions": "Try adjusting your soil conditions or check if data exists in the system."
                }, status=status.HTTP_404_NOT_FOUND)

        # Fixed: Use CropMasterSerializer instead of CropSerializer
        serializer = CropMasterSerializer(crops, many=True)
        print("✅ Recommendations:", [crop['crop_name'] for crop in serializer.data])

        # Save user input to Crop model for tracking
        crop_instance = Crop.objects.create(
            user=request.user,
            soil_texture=soil_texture,
            soil_ph=soil_ph,
            organic_matter=organic_matter,
            drainage_status=drainage_status,
            rainfall_mm=rainfall,
            avg_temperature=temperature,
            sowing_season=data.get('sowing_season', 'Kharif'),
            previous_crop=data.get('previous_crop', 'Unknown'),
            district=data.get('district', 'Unknown'),
            irrigation_type=data.get('irrigation_type', 'Rainfed')
        )

        response_data = {
            "recommendations": serializer.data,
            "total_matches": crops.count(),
            "search_criteria": {
                "soil_texture": soil_texture,
                "drainage_status": drainage_status,
                "organic_matter": organic_matter,
                "soil_ph": soil_ph,
                "rainfall_mm": rainfall,
                "avg_temperature": temperature
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        print("🔥 Unexpected error:", str(e))
        import traceback
        traceback.print_exc()
        return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)