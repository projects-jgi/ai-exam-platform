from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinLengthValidator
from .validators import CollegeEmailValidator

# Add this custom manager class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('hod', 'Head of Department (HOD)'),
        ('admin', 'Super Admin'),
    )
    
    username = None
    email = models.EmailField(
        verbose_name='college email address',
        unique=True,
        validators=[CollegeEmailValidator()],
        help_text='Use your official Jain University email address.'
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student'
    )
    
    # MFA Fields
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Add this line to use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class StudentGroup(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., "MCA ISMS 2024"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': 'student'}
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(5)],
        help_text="Unique student identifier (e.g., Enrollment Number)."
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students' # Access group.students to get all students in a group
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.student_id}"

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': 'faculty'}
    )
    faculty_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(3)]
    )
    department = models.CharField(max_length=100, default="Computer Application")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Prof. {self.user.last_name} ({self.faculty_id})"

    class Meta:
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"


class HODProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': 'hod'}
    )
    faculty_id = models.CharField( # An HOD is also a faculty member, so they have an ID
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(3)]
    )
    department = models.CharField(max_length=100, default="Computer Application")
    # An HOD can be responsible for multiple student groups (e.g., MCA ISMS & MCA General)
    responsible_for_groups = models.ManyToManyField(
        StudentGroup,
        related_name='hods', # Access group.hods to get all HODs for a group
        blank=True,
        help_text="Select the student groups this HOD is responsible for."
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"HOD {self.user.last_name} ({self.faculty_id})"

    class Meta:
        verbose_name = "HOD Profile"
        verbose_name_plural = "HOD Profiles"