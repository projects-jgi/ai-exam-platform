from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from .models import User, StudentProfile, FacultyProfile, HODProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    StudentProfileSerializer, FacultyProfileSerializer, HODProfileSerializer,
    UserProfileSerializer
)

# ===== AUTHENTICATION VIEWS =====

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # After creating user, create corresponding profile based on user_type
            if user.user_type == 'student':
                StudentProfile.objects.create(user=user, student_id=f"STU{user.id:04d}")
            elif user.user_type == 'faculty':
                FacultyProfile.objects.create(user=user, faculty_id=f"FAC{user.id:04d}")
            elif user.user_type == 'hod':
                HODProfile.objects.create(user=user, faculty_id=f"HOD{user.id:04d}")
            
            return Response({
                'message': 'User created successfully. Please log in.',
                'user_id': user.id,
                'user_type': user.user_type
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login_view(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # This creates the session
            return Response({
                'message': 'Login successful',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


# ===== PROFILE VIEWS =====

@api_view(['GET'])
def current_user_profile_view(request):
    """Get the complete profile of the currently logged-in user"""
    user = request.user
    data = {}
    
    # Get the basic user info
    data['user'] = UserProfileSerializer(user).data
    
    # Get the role-specific profile based on user_type
    if user.user_type == 'student':
        profile = get_object_or_404(StudentProfile, user=user)
        data['profile'] = StudentProfileSerializer(profile).data
    elif user.user_type == 'faculty':
        profile = get_object_or_404(FacultyProfile, user=user)
        data['profile'] = FacultyProfileSerializer(profile).data
    elif user.user_type == 'hod':
        profile = get_object_or_404(HODProfile, user=user)
        data['profile'] = HODProfileSerializer(profile).data
    else:  # admin or other types
        data['profile'] = None
    
    return Response(data, status=status.HTTP_200_OK)