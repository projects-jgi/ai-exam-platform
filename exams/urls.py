from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.ExamListView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),  # Added ExamDetailView
    path('exams/<int:exam_id>/start/', views.start_exam_attempt, name='start-exam'),
    
    # CORRECTED: Use only one pattern for each endpoint (removed duplicates)
    path('attempts/<int:attempt_id>/', views.ExamAttemptDetailView.as_view(), name='attempt-detail'),
    path('attempts/<int:attempt_id>/complete/', views.complete_exam_attempt, name='complete-exam'),
    path('attempts/<int:attempt_id>/submit/', views.submit_answer, name='submit-answer'),
]