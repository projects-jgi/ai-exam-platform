from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, StudentProfile, FacultyProfile, HODProfile, StudentGroup

# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)  # Hide password in response

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Use the create_user method from our CustomUserManager to handle password hashing
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data.get('user_type', 'student')
        )
        return user


# Serializer for User Login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Authenticate the user using Django's authentication system
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials. Please try again.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data


# Serializer for Student Group Model
class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = '__all__'  # Serialize all fields: 'id', 'name', 'description'


# Detailed Serializer for User Model (for profile views)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type')


# Serializer for Student Profile (Includes User data)
class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)  # Nest the user info
    group = StudentGroupSerializer(read_only=True)  # Nest the group info
    group_id = serializers.PrimaryKeyRelatedField(  # Allow setting group by ID
        queryset=StudentGroup.objects.all(), source='group', write_only=True, required=False
    )

    class Meta:
        model = StudentProfile
        fields = '__all__'  # Includes 'user', 'student_id', 'group', 'group_id', 'is_active'


# Serializer for Faculty Profile (Includes User data)
class FacultyProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = FacultyProfile
        fields = '__all__'


# Serializer for HOD Profile (Includes User data and Groups)
class HODProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    responsible_for_groups = StudentGroupSerializer(many=True, read_only=True)  # Nest groups info
    group_ids = serializers.PrimaryKeyRelatedField(  # Allow setting groups by list of IDs
        queryset=StudentGroup.objects.all(), source='responsible_for_groups', many=True, write_only=True, required=False
    )

    class Meta:
        model = HODProfile
        fields = '__all__'  # Includes 'user', 'faculty_id', 'department', 'responsible_for_groups', 'group_ids', 'is_active'