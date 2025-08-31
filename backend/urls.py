from django.contrib import admin
from django.urls import path, include  # Add 'include' import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
     path('api/', include('exams.urls')),  # All our API routes will be under /api/
]