from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Exam, ExamAttempt
from core.models import StudentProfile 
from .serializers import ExamSerializer, ExamAttemptSerializer

class ExamListView(generics.ListAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        
        if user.user_type == 'student':
            try:
                student_group = user.studentprofile.group
                return Exam.objects.filter(
                    allowed_groups=student_group,
                    status__in=['scheduled', 'active'],
                    start_time__lte=now,
                    end_time__gte=now
                )
            except StudentProfile.DoesNotExist:
                return Exam.objects.none()
                
        elif user.user_type in ['faculty', 'hod']:
            return Exam.objects.filter(created_by=user)
            
        elif user.user_type == 'admin':
            return Exam.objects.all()
            
        return Exam.objects.none()

class ExamDetailView(generics.RetrieveAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Exam.objects.all()

class ExamAttemptDetailView(generics.RetrieveAPIView):
    serializer_class = ExamAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ExamAttempt.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'attempt_id'

    def get_queryset(self):
        if self.request.user.user_type == 'student':
            return ExamAttempt.objects.filter(student=self.request.user)
        return ExamAttempt.objects.all()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ensure_csrf_cookie
def start_exam_attempt(request, exam_id):
    if request.user.user_type != 'student':
        return Response({'error': 'Only students can attempt exams'}, status=403)
    
    exam = get_object_or_404(Exam, id=exam_id)
    
    try:
        student_group = request.user.studentprofile.group
        if not exam.allowed_groups.filter(id=student_group.id).exists():
            return Response({'error': 'You are not allowed to take this exam'}, status=403)
    except StudentProfile.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=404)
    
    now = timezone.now()
    if now < exam.start_time or now > exam.end_time:
        return Response({'error': 'Exam is not available at this time'}, status=400)
    
    attempt = ExamAttempt.objects.create(
        student=request.user,
        exam=exam,
        attempt_number=1
    )
    
    return Response({
        'attempt_id': attempt.id,
        'message': 'Exam started successfully',
        'duration_minutes': exam.duration_minutes
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ensure_csrf_cookie
def submit_answer(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)
    
    if request.user.user_type == 'student' and attempt.student != request.user:
        return Response({'error': 'Not allowed to submit to this attempt'}, status=403)
    
    if attempt.status != 'in_progress':
        return Response({'error': 'Cannot submit answers to a completed attempt'}, status=400)
    
    return Response({
        'message': 'Answer submission received',
        'attempt_id': attempt_id,
        'status': 'Answer processing will be implemented soon'
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ensure_csrf_cookie
def complete_exam_attempt(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id)
    
    if request.user.user_type == 'student' and attempt.student != request.user:
        return Response({'error': 'Not allowed'}, status=403)
    
    attempt.status = 'submitted'
    attempt.end_time = timezone.now()
    attempt.actual_duration = (attempt.end_time - attempt.start_time).seconds // 60
    attempt.save()
    
    return Response({
        'message': 'Exam completed successfully',
        'score': attempt.score,
        'duration_minutes': attempt.actual_duration
    })