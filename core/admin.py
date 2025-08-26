# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentGroup, StudentProfile, FacultyProfile, HODProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('OTP Info', {'fields': ('otp', 'otp_created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_type'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user_email', 'group', 'is_active')
    list_filter = ('group', 'is_active')
    list_editable = ('is_active',) # Allows toggling active status right from the list view
    search_fields = ('student_id', 'user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user', 'group')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email' # Sets column name in admin


class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user_email', 'department', 'is_active')
    list_filter = ('department', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('faculty_id', 'user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

    def user_email(self, obj):
        return obj.user.email


class HODProfileAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user_email', 'department', 'is_active')
    list_filter = ('department', 'is_active', 'responsible_for_groups')
    list_editable = ('is_active',)
    search_fields = ('faculty_id', 'user__email', 'user__first_name', 'user__last_name')
    filter_horizontal = ('responsible_for_groups',) # Better widget for selecting multiple groups
    raw_id_fields = ('user',)

    def user_email(self, obj):
        return obj.user.email


# Register all models
admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentGroup)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(FacultyProfile, FacultyProfileAdmin)
admin.site.register(HODProfile, HODProfileAdmin)